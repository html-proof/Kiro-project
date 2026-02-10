import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import implicit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle
from typing import List, Dict, Any, Optional


class MetadataRetriever:
    """Handles mapping between item IDs and metadata (title/artist)."""
    
    def __init__(self):
        self._metadata_df = pd.DataFrame()
    
    def load_metadata(self, interactions: List[Dict[str, Any]]):
        """Load metadata from interaction records."""
        if not interactions:
            return
        
        df = pd.DataFrame(interactions)
        
        # Keep newest info for each video_id
        self._metadata_df = df.drop_duplicates('video_id', keep='last').set_index('video_id')
    
    def get_info(self, video_id: str) -> Optional[Dict[str, str]]:
        """Get title and artist for a video ID."""
        if video_id in self._metadata_df.index:
            row = self._metadata_df.loc[video_id]
            return {
                "title": row.get('title'),
                "artist": row.get('artist')
            }
        return None


class InteractionProcessor:
    """Prepares the user-item interaction matrix with advanced weighting."""
    
    def prepare_matrix(self):
        """
        Build interaction matrix from Firebase data.
        
        Weighting scheme:
        - Complete play: +3
        - Partial play: +1
        - Like: +5
        - Skip: -3
        """
        # TODO: Implement efficient way to fetch all interactions
        # For now, return empty dataframes to prevent crash
        plays = []
        likes = []
        skips = []
        
        df_plays = pd.DataFrame(plays)
        df_likes = pd.DataFrame(likes)
        df_skips = pd.DataFrame(skips)
        
        combined = []
        
        # 1. Process Plays (Complete: +3, Partial: +1)
        if not df_plays.empty:
            df_plays['weight'] = df_plays['completed'].apply(lambda x: 3 if x else 1)
            combined.append(df_plays[['user_id', 'video_id', 'weight']])
        
        # 2. Process Likes (+5)
        if not df_likes.empty:
            df_likes['weight'] = 5
            combined.append(df_likes[['user_id', 'video_id', 'weight']])
        
        # 3. Process Skips (-3)
        if not df_skips.empty:
            df_skips['weight'] = -3
            combined.append(df_skips[['user_id', 'video_id', 'weight']])
        
        if not combined:
            return None, None, None, None
        
        full_df = pd.concat(combined)
        
        # Aggregate weights per user-item pair
        agg_df = full_df.groupby(['user_id', 'video_id']).sum().reset_index()
        
        # Mapping for ALS
        agg_df['user_cat'] = agg_df['user_id'].astype('category')
        agg_df['item_cat'] = agg_df['video_id'].astype('category')
        
        user_map = dict(enumerate(agg_df['user_cat'].cat.categories))
        item_map = {id: i for i, id in enumerate(agg_df['item_cat'].cat.categories)}
        reverse_item_map = {i: id for id, i in item_map.items()}
        
        user_ids = agg_df['user_cat'].cat.codes
        item_ids = agg_df['item_cat'].cat.codes
        
        # Create sparse matrix (items x users for implicit library)
        matrix = csr_matrix(
            (agg_df['weight'], (item_ids, user_ids)),
            shape=(len(item_map), len(user_map))
        )
        
        return matrix, user_map, item_map, reverse_item_map


class MLRecommender:
    """
    Machine Learning-based recommendation system.
    
    Features:
    - Collaborative Filtering (ALS)
    - Content-based similarity (TF-IDF)
    - Hybrid recommendations
    """
    
    def __init__(self):
        self.model = None
        self.user_map = {}
        self.item_map = {}
        self.reverse_item_map = {}
        self.retriever = MetadataRetriever()
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.model_path = "models/als_model.pkl"
        
        # Create models directory if it doesn't exist
        if not os.path.exists("models"):
            os.makedirs("models")
    
    def train_als_model(self):
        """Train the ALS collaborative filtering model."""
        processor = InteractionProcessor()
        matrix, u_map, i_map, r_map = processor.prepare_matrix()
        
        if matrix is None:
            print("Insufficient data for ML training.")
            return
        
        self.user_map = u_map
        self.item_map = i_map
        self.reverse_item_map = r_map
        
        # Train ALS model
        self.model = implicit.als.AlternatingLeastSquares(
            factors=50,
            iterations=20,
            regularization=0.1
        )
        self.model.fit(matrix)
        
        # Load metadata for content-based fallback
        try:
            from app.firestore.firestore_client import firestore_client
            all_interactions = firestore_client.get_all_interactions()
            self.retriever.load_metadata(all_interactions)
        except Exception as e:
            print(f"Error loading metadata: {e}")
        
        # Save model
        with open(self.model_path, 'wb') as f:
            pickle.dump(
                (self.model, self.user_map, self.item_map, self.reverse_item_map, self.retriever),
                f
            )
        
        print("ML Recommender trained successfully.")
    
    def load_model(self):
        """Load pre-trained model from disk."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.model, self.user_map, self.item_map, self.reverse_item_map, self.retriever = data
                print("ML model loaded successfully.")
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
                return False
        return False
    
    def get_als_recommendations(self, user_id: str, n: int = 10) -> List[str]:
        """
        Get collaborative filtering recommendations for a user.
        
        Args:
            user_id: User ID
            n: Number of recommendations
            
        Returns:
            List of video IDs
        """
        try:
            # Load model if not already loaded
            if self.model is None:
                if not self.load_model():
                    return []
            
            # Check if user exists in training data
            reverse_user_map = {v: k for k, v in self.user_map.items()}
            if user_id not in reverse_user_map:
                return []
            
            user_idx = reverse_user_map[user_id]
            
            # Get recommendations
            # Create empty user_items matrix (model uses internal data)
            user_items = csr_matrix((1, len(self.item_map)))
            ids, scores = self.model.recommend(user_idx, user_items, N=n)
            
            # Map indices back to video IDs
            return [
                self.reverse_item_map.get(idx) 
                for idx in ids 
                if idx in self.reverse_item_map
            ]
            
        except Exception as e:
            print(f"ALS Recommendation Error: {e}")
            return []
    
    def get_content_similarity(self, song_id: str, n: int = 5) -> List[str]:
        """
        Get content-based similar songs using TF-IDF.
        
        Args:
            song_id: Video ID of the seed song
            n: Number of similar songs
            
        Returns:
            List of similar video IDs
        """
        try:
            df = self.retriever._metadata_df.reset_index()
            
            if df.empty or song_id not in df['video_id'].values:
                return []
            
            # Combine title and artist for content representation
            df['combined'] = df['title'].fillna('') + " " + df['artist'].fillna('')
            
            # Build TF-IDF matrix
            matrix = self.tfidf.fit_transform(df['combined'])
            
            # Find seed song index
            idx = df[df['video_id'] == song_id].index[0]
            
            # Calculate similarity
            sim = cosine_similarity(matrix[idx], matrix).flatten()
            
            # Get top N similar (excluding the seed song itself)
            indices = sim.argsort()[-(n+1):-1][::-1]
            
            return df.iloc[indices]['video_id'].tolist()
            
        except Exception as e:
            print(f"Content Similarity Error: {e}")
            return []
    
    def get_hybrid_recommendations(
        self, 
        user_id: str, 
        seed_song_id: Optional[str] = None,
        n: int = 10
    ) -> List[str]:
        """
        Get hybrid recommendations combining collaborative and content-based.
        
        Args:
            user_id: User ID
            seed_song_id: Optional seed song for content-based
            n: Number of recommendations
            
        Returns:
            List of video IDs
        """
        recommendations = []
        
        # Try collaborative filtering first
        als_recs = self.get_als_recommendations(user_id, n=n)
        recommendations.extend(als_recs)
        
        # If we have a seed song and need more, add content-based
        if seed_song_id and len(recommendations) < n:
            content_recs = self.get_content_similarity(seed_song_id, n=n-len(recommendations))
            recommendations.extend(content_recs)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recs = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recs.append(rec)
        
        return unique_recs[:n]


# Export singleton
ml_recommender = MLRecommender()
