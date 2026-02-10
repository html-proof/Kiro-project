import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  FlatList,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { API_BASE_URL } from '../config/api';
import { colors, spacing, borderRadius, typography, moodColors } from '../config/theme';

const { width } = Dimensions.get('window');

export default function HomeScreen({ navigation }) {
  const [user, setUser] = useState(null);
  const [continueListening, setContinueListening] = useState([]);
  const [autoPlaylists, setAutoPlaylists] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUserData();
    loadContent();
  }, []);

  const loadUserData = async () => {
    const userData = await AsyncStorage.getItem('userData');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  };

  const loadContent = async () => {
    try {
      const token = await AsyncStorage.getItem('userToken');
      
      // Load recent history
      const recentRes = await axios.get(`${API_BASE_URL}/user/recent`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setContinueListening(recentRes.data.slice(0, 5));

      // Load auto playlists
      const playlistsRes = await axios.get(`${API_BASE_URL}/playlist/auto/list`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setAutoPlaylists(playlistsRes.data);
    } catch (error) {
      console.error('Load content error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 18) return 'Good Afternoon';
    return 'Good Evening';
  };

  const moods = [
    { id: 'romantic', name: 'Romantic', icon: '💗', gradient: moodColors.romantic },
    { id: 'party', name: 'Party', icon: '🔥', gradient: moodColors.party },
    { id: 'chill', name: 'Chill', icon: '🌙', gradient: moodColors.chill },
    { id: 'workout', name: 'Workout', icon: '⚡', gradient: moodColors.workout },
    { id: 'sleep', name: 'Sleep', icon: '💤', gradient: moodColors.sleep },
    { id: 'sad', name: 'Sad', icon: '🌧️', gradient: moodColors.sad },
    { id: 'devotional', name: 'Devotional', icon: '🙏', gradient: moodColors.devotional },
    { id: 'motivational', name: 'Motivational', icon: '🚀', gradient: moodColors.motivational },
  ];

  const renderSongCard = ({ item }) => (
    <TouchableOpacity style={styles.songCard}>
      <Image
        source={{ uri: item.thumbnail || 'https://via.placeholder.com/120' }}
        style={styles.songImage}
      />
      <View style={styles.songInfo}>
        <Text style={styles.songTitle} numberOfLines={1}>
          {item.title}
        </Text>
        <Text style={styles.songArtist} numberOfLines={1}>
          {item.artist || 'Unknown Artist'}
        </Text>
      </View>
    </TouchableOpacity>
  );

  const renderAutoPlaylist = ({ item }) => (
    <TouchableOpacity style={styles.playlistCard}>
      <LinearGradient
        colors={['#8B5CF6', '#06B6D4']}
        style={styles.playlistGradient}
      >
        <View style={styles.autoPlaylistBadge}>
          <Text style={styles.autoPlaylistBadgeText}>AUTO</Text>
        </View>
        <Text style={styles.playlistTitle}>{item.name}</Text>
        <Text style={styles.playlistCount}>{item.song_count || 0} songs</Text>
      </LinearGradient>
    </TouchableOpacity>
  );

  const renderMoodTile = ({ item }) => (
    <TouchableOpacity
      style={styles.moodTile}
      onPress={() => navigation.navigate('MoodPlaylist', { mood: item.id })}
    >
      <LinearGradient
        colors={item.gradient}
        style={styles.moodGradient}
      >
        <Text style={styles.moodIcon}>{item.icon}</Text>
        <Text style={styles.moodName}>{item.name}</Text>
      </LinearGradient>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      {/* Aurora Background */}
      <LinearGradient
        colors={['#8B5CF6', '#06B6D4', '#000000']}
        style={styles.auroraBackground}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      />

      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>{getGreeting()}</Text>
            <Text style={styles.userName}>{user?.display_name || 'Music Lover'}</Text>
          </View>
          <TouchableOpacity onPress={() => navigation.navigate('Profile')}>
            {user?.photo_url ? (
              <Image source={{ uri: user.photo_url }} style={styles.avatar} />
            ) : (
              <View style={styles.avatarPlaceholder}>
                <Text style={styles.avatarText}>
                  {user?.display_name?.charAt(0) || 'U'}
                </Text>
              </View>
            )}
          </TouchableOpacity>
        </View>

        {/* Continue Listening */}
        {continueListening.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Continue Listening</Text>
            <FlatList
              horizontal
              data={continueListening}
              renderItem={renderSongCard}
              keyExtractor={(item, index) => `continue-${index}`}
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={styles.horizontalList}
            />
          </View>
        )}

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

        {/* Mood Mosaic */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Mood Mosaic</Text>
          <View style={styles.moodGrid}>
            {moods.map((mood) => (
              <TouchableOpacity
                key={mood.id}
                style={styles.moodTile}
                onPress={() => navigation.navigate('MoodPlaylist', { mood: mood.id })}
              >
                <LinearGradient
                  colors={mood.gradient}
                  style={styles.moodGradient}
                >
                  <Text style={styles.moodIcon}>{mood.icon}</Text>
                  <Text style={styles.moodName}>{mood.name}</Text>
                </LinearGradient>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Data Saver Badge */}
        <View style={styles.dataSaverBadge}>
          <Text style={styles.dataSaverText}>🎵 Smart Data Saver ON</Text>
        </View>

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
  auroraBackground: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 300,
    opacity: 0.15,
  },
  scrollView: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.xxl + 20,
    paddingBottom: spacing.lg,
  },
  greeting: {
    ...typography.caption,
    marginBottom: spacing.xs,
  },
  userName: {
    ...typography.h2,
  },
  avatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    borderWidth: 2,
    borderColor: colors.primary,
  },
  avatarPlaceholder: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.textPrimary,
  },
  section: {
    marginBottom: spacing.xl,
  },
  sectionTitle: {
    ...typography.h3,
    paddingHorizontal: spacing.lg,
    marginBottom: spacing.md,
  },
  horizontalList: {
    paddingHorizontal: spacing.lg,
  },
  songCard: {
    width: 160,
    marginRight: spacing.md,
    backgroundColor: colors.backgroundCard,
    borderRadius: borderRadius.md,
    overflow: 'hidden',
  },
  songImage: {
    width: '100%',
    height: 160,
    backgroundColor: colors.backgroundElevated,
  },
  songInfo: {
    padding: spacing.sm,
  },
  songTitle: {
    ...typography.body,
    marginBottom: spacing.xs,
  },
  songArtist: {
    ...typography.caption,
  },
  playlistCard: {
    width: 200,
    height: 120,
    marginRight: spacing.md,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
  },
  playlistGradient: {
    flex: 1,
    padding: spacing.md,
    justifyContent: 'flex-end',
  },
  autoPlaylistBadge: {
    position: 'absolute',
    top: spacing.sm,
    right: spacing.sm,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.sm,
  },
  autoPlaylistBadgeText: {
    fontSize: 10,
    fontWeight: 'bold',
    color: colors.textPrimary,
  },
  playlistTitle: {
    ...typography.h3,
    marginBottom: spacing.xs,
  },
  playlistCount: {
    ...typography.caption,
  },
  moodGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingHorizontal: spacing.lg,
  },
  moodTile: {
    width: (width - spacing.lg * 2 - spacing.md) / 2,
    height: 100,
    marginRight: spacing.md,
    marginBottom: spacing.md,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
  },
  moodGradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  moodIcon: {
    fontSize: 32,
    marginBottom: spacing.xs,
  },
  moodName: {
    ...typography.body,
    fontWeight: '600',
  },
  dataSaverBadge: {
    marginHorizontal: spacing.lg,
    marginTop: spacing.lg,
    padding: spacing.md,
    backgroundColor: colors.glassBackground,
    borderRadius: borderRadius.md,
    borderWidth: 1,
    borderColor: colors.glassBorder,
    alignItems: 'center',
  },
  dataSaverText: {
    ...typography.caption,
    color: colors.primary,
  },
});
</Text>