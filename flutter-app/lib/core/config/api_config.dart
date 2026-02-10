class ApiConfig {
  // Your Railway Backend URL
  static const String baseUrl = 'https://web-production-1dedc.up.railway.app';
  
  // API Endpoints
  static const String search = '/search';
  static const String audio = '/audio';
  static const String video = '/video';
  static const String streamAudio = '/stream/audio';
  static const String streamVideo = '/stream/video';
  static const String preview = '/preview';
  
  // Auth
  static const String authLogin = '/auth/login';
  static const String authVerify = '/auth/verify';
  
  // User
  static const String userPreferences = '/user/preferences';
  static const String userPlay = '/user/play';
  static const String userProgress = '/user/progress';
  static const String userLike = '/user/like';
  static const String userHistory = '/user/history';
  static const String userLikes = '/user/likes';
  static const String userRecent = '/user/recent';
  static const String userRecommend = '/user/recommend';
  
  // Playlists
  static const String playlistCreate = '/playlist/create';
  static const String playlistAll = '/playlist/all';
  
  // Auto Playlists
  static const String autoPlaylistOnRepeat = '/playlist/auto/on-repeat';
  static const String autoPlaylistDailyMix = '/playlist/auto/daily-mix';
  static const String autoPlaylistRecent = '/playlist/auto/recently-played';
  static const String autoPlaylistLiked = '/playlist/auto/liked-songs';
  
  // Recommendations
  static const String recommendType = '/recommend/type';
  static const String recommendArtist = '/recommend/artist';
  static const String recommendSimilar = '/recommend/similar';
  static const String recommendBecauseLiked = '/recommend/because-liked';
  
  // Quality options
  static const List<String> audioQualities = ['ultra', 'saver', 'high'];
  static const List<String> videoQualities = ['high', 'medium', 'low'];
  
  // Default quality
  static const String defaultAudioQuality = 'saver';
  static const String defaultVideoQuality = 'medium';
}
