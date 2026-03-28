import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, Alert } from 'react-native';
import * as Notifications from 'expo-notifications';

// Set up Expo notification handler for foreground behavior
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: false,
    shouldSetBadge: false,
  }),
});

// The URL of your agentic-notify FastAPI server
const BACKEND_URL = 'http://localhost:8000/events/ingest';

export default function App() {
  const [lastEventId, setLastEventId] = useState<string | null>(null);

  useEffect(() => {
    // Request permission (iOS/Android 13+)
    Notifications.requestPermissionsAsync().then(({ status }) => {
      if (status !== 'granted') {
        Alert.alert('Permission needed for notifications');
      }
    });

    // Listener for when a notification is clicked or received
    const subscription = Notifications.addNotificationReceivedListener(notification => {
      console.log('Notification received:', notification);
      
      const payload = {
        event_id: notification.request.identifier,
        source_platform: 'react_native_expo',
        source_app: 'open_notify',
        title: notification.request.content.title || '',
        body: notification.request.content.body || '',
        received_at: new Date().toISOString(),
        metadata: notification.request.content.data || {}
      };

      setLastEventId(payload.event_id);
      sendToAgenticBackend(payload);
    });

    return () => subscription.remove();
  }, []);

  const sendToAgenticBackend = async (payload: any) => {
    try {
      const response = await fetch(BACKEND_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      console.log('Backend orchestrator response:', data);
    } catch (error) {
      console.error('Failed to send notification to backend:', error);
    }
  };

  const triggerTestNotification = async () => {
    await Notifications.scheduleNotificationAsync({
      content: {
        title: "Interview Request",
        body: "You have a new interview scheduled for 2:00 PM tomorrow.",
        data: { importance: 'high' },
      },
      trigger: { seconds: 2 },
    });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>OpenNotify Mobile Bridge</Text>
      <Text style={styles.subtitle}>Listens for OS notifications and routes them to the Agentic Python Backend.</Text>
      
      <View style={styles.button} onTouchEnd={triggerTestNotification}>
        <Text style={styles.buttonText}>Simulate Incoming Notification</Text>
      </View>
      
      {lastEventId && (
        <Text style={styles.status}>Sent event: {lastEventId}</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 10 },
  subtitle: { textAlign: 'center', marginBottom: 30, color: '#666' },
  button: { backgroundColor: '#007AFF', padding: 15, borderRadius: 8 },
  buttonText: { color: 'white', fontWeight: 'bold' },
  status: { marginTop: 20, fontFamily: 'monospace', color: 'green' }
});
