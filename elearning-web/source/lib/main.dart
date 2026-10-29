import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:syncfusion_flutter_core/core.dart';
import 'minicloud_bootstrap.dart';
import 'presentation/widgets/auth/auth_wrapper.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  const license = String.fromEnvironment('SYNCFUSION_LICENSE');
  if (license.isNotEmpty) SyncfusionLicense.registerLicense(license);
  await initializeMiniCloudDemo();
  runApp(const ProviderScope(child: AuthWrapper()));
}
