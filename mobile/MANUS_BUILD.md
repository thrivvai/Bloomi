# Bloomi — EAS Build Guide for Manus

## Prerequisites

1. **Expo account** — create one at expo.dev if you don't have one
2. **EAS CLI** — `npm install -g eas-cli`
3. **EXPO_TOKEN** — generate at expo.dev → Account → Access Tokens
4. **Font files** — place in `assets/fonts/` (see `assets/README.md`)
5. **Image assets** — place in `assets/` (see `assets/README.md`)

## One-time setup

```bash
# Clone the repo
git clone https://github.com/thrivvai/Bloomi.git
cd Bloomi/mobile

# Install dependencies
npm install

# Log in to EAS
eas login
# or set EXPO_TOKEN env var

# Link to your Expo project (run once)
eas init --id <your-expo-project-id>
# Update the projectId in app.json → extra.eas.projectId
```

## Build the AAB (internal track)

```bash
cd Bloomi/mobile
eas build --platform android --profile internal
```

This produces an `.aab` file you can download and submit to Google Play.

## Build profiles

| Profile | Output | Use case |
|---------|--------|----------|
| `development` | APK (debug) | Local testing with Expo Go dev client |
| `preview` | APK (release) | Internal testers via APK install |
| `internal` | AAB (release) | Google Play internal testing track |
| `production` | AAB (release) | Google Play production track |

## Submit to Google Play

```bash
# After a successful internal build
eas submit --platform android --profile production
# Requires google-services-key.json in mobile/ (NOT committed — add to CI secrets)
```

## Environment variables

| Variable | Where to set | Description |
|----------|-------------|-------------|
| `EXPO_PUBLIC_API_URL` | `.env` or EAS secrets | Backend API base URL |
| `EXPO_TOKEN` | CI secrets | EAS authentication token |

## GitHub Actions

Trigger a build from the Actions tab → "EAS Build (Android AAB)" → choose profile.
Requires `EXPO_TOKEN` set as a repository secret.
