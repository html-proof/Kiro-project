import re


class TrustedChannels:
    def __init__(self):
        # 1. GLOBAL TOP LABELS
        self.GLOBAL_LABELS = [
            "vevo", "topic", "official audio", "official video",
            "sony music", "universal music", "warner records", "atlantic records", 
            "republic records", "interscope records", "capitol records", "rca records", 
            "columbia records", "def jam", "island records", "epic records", 
            "vevo", "umg", "wmg", "sme"
        ]
        
        # 2. INDIAN MAJOR LABELS - EXPANDED FOR ALL LANGUAGES & MOODS
        self.INDIAN_LABELS = [
            # Hindi/Bollywood Majors
            "t-series", "zee music", "saregama", "tips official",
            "yrf", "times music", "sony music india", "think music",
            
            # Telugu/Tollywood
            "aditya music", "volga video", "ananda audio", "larsc entertainment",
            
            # Tamil/Kollywood  
            "saregama tamil", "think music india", "d imman music", "sowkya music",
            
            # Kannada/Sandalwood
            "lahari music", "anand audio", "paramvah studios", "msil music",
            
            # Malayalam/Mollywood
            "manorama music", "muzik247", "satyam audios", "millennium audios",
            "jax music", "swargachitra", "century music", "sony music malayalam",
            
            # Punjabi/Punjab
            "speed records", "white hill music", "jass records", "djjass records",
            "r-nation", "fresh touch entertainment", "mp4 music", "b ally music",
            
            # Marathi
            "zee music marathi", "tips marathi", "shree ashtavinayak", "atharva entertainment",
            
            # Bengali/Tollywood (Bengal)
            "svf music", "times music bangla", "shree venkatesh films", "grassroot entertainment",
            
            # Odia
            "saregama odia", "dreams odia", "cuttack records", "odisha music",
            
            # Gujarati
            "shemaroo gujarati", "zee music gujarati", "saanjh music", "rf music"
        ]
        
        # 3. K-POP / J-POP
        self.EAST_ASIAN_LABELS = [
            "hybe labels", "sm entertainment", "jyp entertainment", 
            "yg entertainment", "stone music", "avex", "king records"
        ]
        
        # 4. REGIONAL SPECIALS (UAE/EU/Middle East)
        self.REGIONAL_LABELS = [
            "rotana music", "platinum records", "mazzika", 
            "spinnin' records", "armada music", "ministry of sound",
            "nexus music", "anghami"
        ]
        
        # 5. LIVE MUSIC CHANNELS (Reliable Indian & Global)
        self.LIVE_MUSIC_LABELS = [
            # Indian Live Music Channels
            "sonyliv music", "zee5 music", "gaana live", "jiosaavn live",
            "tips live", "saregama live", "speed live", "white hill live",
            "manorama music live", "aditya music live", "lahari live",
            
            # Global Live Music
            "vevo live", "mtv live", "vh1 live", "colors live",
            "mtv unplugged", "mtv unclogged", "live nation", "live from here",
            
            # Regional Live
            "rotana live", "mazhavil manorama live", "asianet music live"
        ]
        
        # 5. HARD NON-MUSIC BLOCK LIST
        self.HARD_BLOCK_KEYWORDS = [
            "trailer", "teaser", "scene", "movie", "film", "cinema",
            "full movie", "climax", "dialogue", "comedy", "fight",
            "news", "live news", "breaking", "report", "journalist",
            "media", "press", "debate", "interview", "speech", 
            "motivation", "explained", "review", "reaction", "vlog", "shorts"
        ]
        
        # 6. MUSIC SPAM BLOCK LIST
        self.SPAM_KEYWORDS = [
            "8d", "3d", "spatial", "360",
            "slowed", "reverb", "nightcore", "sped up", "speed up",
            "bass boosted", "boosted", "karaoke", "instrumental",
            "remix", "dj", "mix", "mashup", "bgm", "background music",
            "status", "edit", "tiktok"
        ]
        
        self.ALL_TRUSTED = (
            self.GLOBAL_LABELS + 
            self.INDIAN_LABELS + 
            self.EAST_ASIAN_LABELS + 
            self.REGIONAL_LABELS +
            self.LIVE_MUSIC_LABELS
        )
    
    def normalize(self, text: str) -> str:
        """Normalize text for comparison by lowercasing and removing special chars."""
        if not text:
            return ""
        text = text.lower().strip()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text
    
    def calculate_trust_score(self, channel_name: str, video_title: str) -> int:
        """Calculate trust score based on channel name and video title."""
        c = self.normalize(channel_name)
        t = self.normalize(video_title)
        score = 0
        
        # Match trusted channel words (including LIVE)
        if any(label in c for label in self.ALL_TRUSTED):
            score += 50
        
        # High Priority Identifiers
        if "vevo" in c or "vevo" in t:
            score += 40
        if "topic" in c:
            score += 40
        
        # LIVE MUSIC BOOSTERS
        live_signals = ["live performance", "live session", "unplugged",
                        "live concert", "live show", "acoustic live"]
        if any(signal in t for signal in live_signals):
            score += 30
        elif "live" in t and "music" in t:
            score += 25  # Legitimate live music
        
        # Audio Quality Identifiers
        audio_signals = ["official audio", "official music video", "song", "audio"]
        if any(signal in t for signal in audio_signals):
            score += 20
        elif "official" in t:
            score += 10
        
        return score
    
    def is_spam(self, title: str, query: str) -> bool:
        """Check if content should be filtered as spam."""
        t = self.normalize(title)
        q = self.normalize(query)
        
        # 1. Hard block non-music content
        if any(k in t for k in self.HARD_BLOCK_KEYWORDS):
            return True
        
        # 2. Block spam music types unless user specifically asked for them
        for word in self.SPAM_KEYWORDS:
            if word in t and word not in q:
                return True
        
        return False


# Export singleton
trusted_channels = TrustedChannels()
