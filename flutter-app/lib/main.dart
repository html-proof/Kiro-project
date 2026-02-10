import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'core/config/theme_config.dart';
import 'core/di/injection.dart';
import 'features/splash/splash_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase
  await Firebase.initializeApp();
  
  // Initialize Hive
  await Hive.initFlutter();
  
  // Initialize Dependency Injection
  setupDependencies();
  
  // Set system UI
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
    ),
  );
  
  // Lock portrait orientation
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
  ]);
  
  runApp(const ProviderScope(child: MusiclyApp()));
}

class MusiclyApp extends StatelessWidget {
  const MusiclyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Musicly',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      home: const SplashScreen(),
    );
  }
}
