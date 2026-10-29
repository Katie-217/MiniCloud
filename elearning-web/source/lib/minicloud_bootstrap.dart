import 'package:firebase_core/firebase_core.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:cloud_functions/cloud_functions.dart';

/// This adaptation has no production Firebase project configuration.
Future<void> initializeMiniCloudDemo() async {
  await Firebase.initializeApp(options: const FirebaseOptions(
    apiKey: 'demo-minicloud-emulator-key',
    appId: '1:123456789:web:minicloud-demo',
    messagingSenderId: '123456789',
    projectId: 'demo-minicloud',
    authDomain: 'localhost',
    storageBucket: 'demo-minicloud.appspot.com',
  ));
  final host = Uri.base.host;
  FirebaseFirestore.instance.settings = const Settings(
    persistenceEnabled: false, webExperimentalForceLongPolling: true,
  );
  FirebaseFirestore.instance.useFirestoreEmulator(host, 8180);
  await FirebaseStorage.instance.useStorageEmulator(host, 9199);
  // Link preview is optional and has no deployed function in the local demo.
  FirebaseFunctions.instance.useFunctionsEmulator(host, 5001);
}
