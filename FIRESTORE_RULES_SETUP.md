# 🔒 Firestore Security Rules Setup

Complete guide to implement security rules for your Musicly Backend.

---

## 📋 What These Rules Do

### ✅ Security Features

1. **User Isolation**
   - Users can ONLY access their own data
   - Cannot read/write other users' data
   - Enforced at database level

2. **Authentication Required**
   - All operations require Firebase authentication
   - No anonymous access
   - Token verification automatic

3. **Data Integrity**
   - Users can't change their own UID
   - Video IDs must match document IDs
   - Playlist IDs must match document IDs

4. **Prevent Deletion**
   - User profiles cannot be deleted
   - Protects against accidental data loss

5. **Subcollection Protection**
   - Likes, history, playlists all protected
   - Each user's data is isolated
   - No cross-user access

---

## 🚀 Quick Setup (2 Minutes)

### Method 1: Firebase Console (Recommended)

1. **Go to Firestore Rules:**
   https://console.firebase.google.com/project/music-app-f2e65/firestore/rules

2. **Copy the rules from `firestore.rules` file**

3. **Paste into the editor**

4. **Click "Publish"**

Done! ✅

### Method 2: Firebase CLI

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize (if not done)
firebase init firestore

# Deploy rules
firebase deploy --only firestore:rules
```

---

## 📖 Rules Explanation

### User Profile Rules

```javascript
match /users/{userId} {
  // Users can read their own profile
  allow read: if isOwner(userId);
  
  // Users can create their own profile
  allow create: if isAuthenticated() && 
                   request.auth.uid == userId;
  
  // Users can update their own profile
  allow update: if isOwner(userId);
  
  // Users CANNOT delete their profile
  allow delete: if false;
}
```

### Likes Rules

```javascript
match /users/{userId}/likes/{videoId} {
  // Only owner can read their likes
  allow read: if isOwner(userId);
  
  // Only owner can add likes
  allow create: if isOwner(userId);
  
  // Only owner can update likes
  allow update: if isOwner(userId);
  
  // Only owner can remove likes
  allow delete: if isOwner(userId);
}
```

### History Rules

```javascript
match /users/{userId}/history/{historyId} {
  // Only owner can access their history
  allow read, write: if isOwner(userId);
}
```

### Playlist Rules

```javascript
match /users/{userId}/playlists/{playlistId} {
  // Only owner can access their playlists
  allow read, write: if isOwner(userId);
  
  // Playlist songs
  match /songs/{videoId} {
    allow read, write: if isOwner(userId);
  }
}
```

### Auto Playlist Rules

```javascript
match /users/{userId}/auto_playlists/{playlistId} {
  // Only owner can access auto playlists
  allow read, write: if isOwner(userId);
  
  // Auto playlist songs
  match /songs/{videoId} {
    allow read, write: if isOwner(userId);
  }
}
```

---

## 🧪 Testing the Rules

### Test 1: User Can Access Own Data

```javascript
// This should SUCCEED
const userId = auth.currentUser.uid;
const userDoc = await db.collection('users').doc(userId).get();
```

### Test 2: User Cannot Access Other's Data

```javascript
// This should FAIL
const otherUserId = 'some-other-user-id';
const userDoc = await db.collection('users').doc(otherUserId).get();
// Error: Missing or insufficient permissions
```

### Test 3: Unauthenticated Access Denied

```javascript
// This should FAIL
// Without authentication
const userDoc = await db.collection('users').doc('any-user').get();
// Error: Missing or insufficient permissions
```

### Test 4: User Can Create Own Profile

```javascript
// This should SUCCEED
const userId = auth.currentUser.uid;
await db.collection('users').doc(userId).set({
  uid: userId,
  email: 'user@example.com',
  name: 'John Doe'
});
```

---

## 🔍 Rules Simulator

Test your rules in Firebase Console:

1. Go to: https://console.firebase.google.com/project/music-app-f2e65/firestore/rules
2. Click **"Rules Playground"** tab
3. Test different scenarios:

**Example Test:**
```
Location: /users/user123
Authenticated: Yes
Auth UID: user123
Operation: get

Result: ✅ Allowed
```

**Example Test (Should Fail):**
```
Location: /users/user123
Authenticated: Yes
Auth UID: user456
Operation: get

Result: ❌ Denied
```

---

## 📊 Database Structure (Protected)

```
users/{uid}                           ← Protected by isOwner()
  ├── uid: string
  ├── email: string
  ├── name: string
  ├── photo_url: string
  ├── selected_languages: array
  ├── selected_artists: array
  └── created_at: timestamp

users/{uid}/likes/{video_id}         ← Protected by isOwner()
  ├── video_id: string
  ├── title: string
  ├── artist: string
  ├── thumbnail: string
  ├── duration: number
  └── liked_at: timestamp

users/{uid}/history/{auto_id}        ← Protected by isOwner()
  ├── video_id: string
  ├── title: string
  ├── played_at: timestamp
  └── ...

users/{uid}/playlists/{playlist_id}  ← Protected by isOwner()
  ├── playlist_id: string
  ├── name: string
  └── ...
  
  └── songs/{video_id}                ← Protected by isOwner()
      ├── video_id: string
      ├── title: string
      └── ...

users/{uid}/auto_playlists/{id}      ← Protected by isOwner()
  └── songs/{video_id}                ← Protected by isOwner()
```

---

## 🛡️ Security Best Practices

### ✅ DO:

1. **Always authenticate users**
   ```javascript
   const token = await user.getIdToken();
   // Send token to backend
   ```

2. **Use backend for sensitive operations**
   - Backend uses Admin SDK (bypasses rules)
   - Backend validates user tokens
   - Backend enforces business logic

3. **Keep rules simple**
   - Current rules are clear and maintainable
   - Easy to understand and audit

4. **Test rules regularly**
   - Use Rules Playground
   - Test edge cases
   - Verify security

### ❌ DON'T:

1. **Don't use test mode in production**
   ```javascript
   // BAD - allows anyone to read/write
   allow read, write: if true;
   ```

2. **Don't trust client-side validation**
   - Always validate on backend
   - Rules are last line of defense

3. **Don't expose sensitive data**
   - Keep API keys secure
   - Don't store passwords in Firestore

4. **Don't allow anonymous access**
   - Always require authentication
   - No public data in this app

---

## 🚨 Common Issues

### Issue: "Missing or insufficient permissions"

**Cause:** User not authenticated or accessing wrong data

**Solution:**
```javascript
// Make sure user is authenticated
const user = auth.currentUser;
if (!user) {
  // Redirect to login
}

// Make sure accessing own data
const userId = user.uid;
const userDoc = await db.collection('users').doc(userId).get();
```

### Issue: "Permission denied" on create

**Cause:** UID mismatch or wrong document ID

**Solution:**
```javascript
// Correct way
const userId = auth.currentUser.uid;
await db.collection('users').doc(userId).set({
  uid: userId,  // Must match
  email: 'user@example.com'
});
```

### Issue: Rules not updating

**Cause:** Rules not published or cached

**Solution:**
1. Click "Publish" in Firebase Console
2. Wait 1-2 minutes for propagation
3. Clear browser cache if needed

---

## 📝 Development vs Production Rules

### Development (Test Mode)

For initial development, you can use test mode:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.time < timestamp.date(2026, 3, 1);
    }
  }
}
```

**⚠️ WARNING:** This allows anyone to read/write until March 1, 2026!

### Production (Secure Mode)

Use the rules in `firestore.rules` file for production.

---

## 🔄 Updating Rules

### When to Update:

1. **Adding new collections**
   - Add rules for new collections
   - Test thoroughly

2. **Changing data structure**
   - Update validation rules
   - Test with new structure

3. **Adding features**
   - Add rules for new features
   - Maintain security

### How to Update:

1. Edit `firestore.rules` file
2. Test in Rules Playground
3. Deploy via Console or CLI
4. Verify in production

---

## ✅ Verification Checklist

After deploying rules:

- [ ] Rules published successfully
- [ ] Users can read own data
- [ ] Users cannot read others' data
- [ ] Unauthenticated access denied
- [ ] Can create own profile
- [ ] Can add likes
- [ ] Can create playlists
- [ ] Can track history
- [ ] Cannot delete user profile
- [ ] Backend operations work (Admin SDK)

---

## 🔗 Quick Links

- **Firestore Rules:** https://console.firebase.google.com/project/music-app-f2e65/firestore/rules
- **Rules Playground:** https://console.firebase.google.com/project/music-app-f2e65/firestore/rules (Rules Playground tab)
- **Firestore Data:** https://console.firebase.google.com/project/music-app-f2e65/firestore/data
- **Firebase Docs:** https://firebase.google.com/docs/firestore/security/get-started

---

## 📞 Support

If you encounter issues:

1. Check **TROUBLESHOOTING.md**
2. Test in Rules Playground
3. Verify authentication is working
4. Check backend logs

---

**Your Firestore is now secure! 🔒**

Rules are in: `firestore.rules`  
Deploy at: https://console.firebase.google.com/project/music-app-f2e65/firestore/rules
