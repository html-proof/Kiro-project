import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  FlatList,
  Image,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { API_BASE_URL } from '../config/api';
import { colors, spacing, borderRadius, typography } from '../config/theme';

export default function LibraryScreen({ navigation }) {
  const [likedSongs, setLikedSongs] = useState([]);
  const [autoPlaylists, setAutoPlaylists] = useState([]);
  const [userPlaylists, setUserPlaylists] = useState([]);
  const [recentlyPlayed, setRecentlyPlayed] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLibrary();
  }, []);

  const loadLibrary = async () => {
    try {
      const token = await AsyncStorage.getItem('userToken');

      // Load liked songs
      const likesRes = await axios.get(`${API_BASE_URL}/user/likes`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setLikedSongs(likesRes.data);

      // Load auto playlists
      const autoRes = await axios.get(`${API_BASE_URL}/playlist/auto/list`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setAutoPlaylists(autoRes.data);

      // Load user playlists
      const playlistsRes = await axios.get(`${API_BASE_URL}/playlist/list`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUserPlaylists(playlistsRes.data);

      // Load recently played
      const recentRes = await axios.get(`${API_BASE_URL}/user/recent`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setRecentlyPlayed(recentRes.data.slice(0, 10));
    } catch (error) {
      console.error('Load library error:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderAutoPlaylist = ({ item }) => (
    <TouchableOpacity
      style={styles.autoPlaylistCard}
      onPress={() => navigation.navigate('PlaylistDetail', { playlist: item })}
    >
      <LinearGradient
        colors={['#8B5CF6', '#06B6D4']}
        style={styles.playlistGradient}
      >
        <View style={styles.autoBadge}>
          <Text style={styles.autoBadgeText}>AUTO</Text>
        </View>
        <Text style={styles.playlistTitle}>{item.name}</Text>
        <Text style={styles.playlistCount}>
          {item.song_count || 0} songs
        </Text>
      </LinearGradient>
    </TouchableOpacity>
  );

  const renderUserPlaylist = ({ item }) => (
    <TouchableOpacity
      style={styles.userPlaylistCard}
      onPress={() => navigation.navigate('PlaylistDetail', { playlist: item })}
    >
      <View style={styles.playlistCover}>
        <Text style={styles.playlistCoverIcon}>🎵</Text>
      </View>
      <Text style={styles.userPlaylistTitle} numberOfLines={1}>
        {item.name}
      </Text>
      <Text style={styles.userPlaylistCount}>
        {item.songs?.length || 0} songs
      </Text>
    </TouchableOpacity>
  );

  const renderRecentSong = ({ item }) => (
    <TouchableOpacity
      style={styles.recentSongItem}
      onPress={() => navigation.navigate('Player', { song: item })}
    >
      <Image
        source={{ uri: item.thumbnail || 'https://via.placeholder.com/50' }}
        style={styles.recentThumbnail}
      />
      <View style={styles.recentInfo}>
        <Text style={styles.recentTitle} numberOfLines={1}>
          {item.title}
        </Text>
        <Text style={styles.recentArtist} numberOfLines={1}>
          {item.artist || 'Unknown Artist'}
        </Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Library</Text>
        </View>

        {/* Liked Songs */}
        <TouchableOpacity
          style={styles.likedSongsCard}
          onPress={() => navigation.navigate('LikedSongs')}
        >
          <LinearGradient
            colors={['#EC4899', '#F472B6']}
            style={styles.likedGradient}
          >
            <Text style={styles.likedIcon}>❤️</Text>
            <Text style={styles.likedTitle}>Liked Songs</Text>
            <Text style={styles.likedCount}>
              {likedSongs.length} songs
            </Text>
          </LinearGradient>
        </TouchableOpacity>

        {/* Auto Playlists */}
        {autoPlaylists.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Auto Playlists</Text>
            <FlatList
              horizontal
              data={autoPlaylists}
              renderItem={renderAutoPlaylist}
              keyExtractor={(item) => item.playlist_id}
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={styles.horizontalList}
            />
          </View>
        )}

        {/* Your Playlists */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Your Playlists</Text>
            <TouchableOpacity
              onPress={() => navigation.navigate('CreatePlaylist')}
            >
              <Text style={styles.createButton}>+ Create</Text>
            </TouchableOpacity>
          </View>
          {userPlaylists.length > 0 ? (
            <FlatList
              horizontal
              data={userPlaylists}
              renderItem={renderUserPlaylist}
              keyExtractor={(item) => item.playlist_id}
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={styles.horizontalList}
            />
          ) : (
            <Text style={styles.emptyText}>
              No playlists yet. Create your first playlist!
            </Text>
          )}
        </View>

        {/* Recently Played */}
        {recentlyPlayed.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Recently Played</Text>
            <FlatList
              data={recentlyPlayed}
              renderItem={renderRecentSong}
              keyExtractor={(item, index) => `recent-${index}`}
              scrollEnabled={false}
            />
          </View>
        )}

        <View style={{ height: 100 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.xxl + 20,
    paddingBottom: spacing.lg,
  },
  headerTitle: {
    ...typography.h1,
  },
  likedSongsCard: {
    marginHorizontal: spacing.lg,
    marginBottom: spacing.xl,
    height: 120,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
  },
  likedGradient: {
    flex: 1,
    padding: spacing.lg,
    justifyContent: 'center',
  },
  likedIcon: {
    fontSize: 32,
    marginBottom: spacing.sm,
  },
  likedTitle: {
    ...typography.h2,
    marginBottom: spacing.xs,
  },
  likedCount: {
    ...typography.caption,
  },
  section: {
    marginBottom: spacing.xl,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
    marginBottom: spacing.md,
  },
  sectionTitle: {
    ...typography.h3,
  },
  createButton: {
    ...typography.body,
    color: colors.primary,
    fontWeight: '600',
  },
  horizontalList: {
    paddingHorizontal: spacing.lg,
  },
  autoPlaylistCard: {
    width: 180,
    height: 100,
    marginRight: spacing.md,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
  },
  playlistGradient: {
    flex: 1,
    padding: spacing.md,
    justifyContent: 'flex-end',
  },
  autoBadge: {
    position: 'absolute',
    top: spacing.sm,
    right: spacing.sm,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.sm,
  },
  autoBadgeText: {
    fontSize: 10,
    fontWeight: 'bold',
    color: colors.textPrimary,
  },
  playlistTitle: {
    ...typography.h3,
    fontSize: 16,
    marginBottom: spacing.xs,
  },
  playlistCount: {
    ...typography.caption,
    fontSize: 12,
  },
  userPlaylistCard: {
    width: 140,
    marginRight: spacing.md,
  },
  playlistCover: {
    width: 140,
    height: 140,
    backgroundColor: colors.backgroundCard,
    borderRadius: borderRadius.md,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  playlistCoverIcon: {
    fontSize: 48,
  },
  userPlaylistTitle: {
    ...typography.body,
    marginBottom: spacing.xs,
  },
  userPlaylistCount: {
    ...typography.caption,
  },
  recentSongItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
  },
  recentThumbnail: {
    width: 50,
    height: 50,
    borderRadius: borderRadius.sm,
    backgroundColor: colors.backgroundCard,
  },
  recentInfo: {
    flex: 1,
    marginLeft: spacing.md,
  },
  recentTitle: {
    ...typography.body,
    marginBottom: spacing.xs,
  },
  recentArtist: {
    ...typography.caption,
  },
  emptyText: {
    ...typography.body,
    color: colors.textSecondary,
    paddingHorizontal: spacing.lg,
    textAlign: 'center',
  },
});
