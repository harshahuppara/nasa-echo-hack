/**
 * Mars Equipment Assets Configuration
 * Maps Opportunity, Viking 1, and Ingenuity to their GLB 3D models and audio stories.
 */
const MARS_EQUIPMENT_ASSETS = {
  "opportunity": {
    id: "opportunity",
    name: "Opportunity",
    type: "Rover",
    aliasIds: ["opportunity-rover", "opportunity", "oppy", "mer-b", "mer_b"],
    modelFiles: [
      "/app/static/models/Oppurtunity%20.glb",
      "/static/models/Oppurtunity%20.glb",
      "static/models/Oppurtunity%20.glb",
      "models/Oppurtunity%20.glb"
    ],
    audioFiles: [
      "/app/static/audio/SPIRIT%20AND%20OPPURTUNITY%20MARS.mp3",
      "/static/audio/SPIRIT%20AND%20OPPURTUNITY%20MARS.mp3",
      "static/audio/SPIRIT%20AND%20OPPURTUNITY%20MARS.mp3",
      "audio/SPIRIT%20AND%20OPPURTUNITY%20MARS.mp3"
    ],
    color: "#38bdf8"
  },
  "viking-1": {
    id: "viking-1",
    name: "Viking 1",
    type: "Lander",
    aliasIds: ["viking-1-lander", "viking-1", "viking1", "viking_1", "viking-lander", "viking_one", "viking"],
    modelFiles: [
      "/app/static/models/Viking%20Lander%20.glb",
      "/static/models/Viking%20Lander%20.glb",
      "static/models/Viking%20Lander%20.glb",
      "models/Viking%20Lander%20.glb"
    ],
    audioFiles: [
      "/app/static/audio/VIKING%20MARS.mp3",
      "/static/audio/VIKING%20MARS.mp3",
      "static/audio/VIKING%20MARS.mp3",
      "audio/VIKING%20MARS.mp3"
    ],
    color: "#a855f7"
  },
  "ingenuity": {
    id: "ingenuity",
    name: "Ingenuity",
    type: "Helicopter",
    aliasIds: ["ingenuity-helicopter", "ingenuity", "ingenuity_helicopter", "mars_helicopter", "heli"],
    modelFiles: [
      "/app/static/models/Ingenuity%20Mars%20Helicopter%20.glb",
      "/static/models/Ingenuity%20Mars%20Helicopter%20.glb",
      "static/models/Ingenuity%20Mars%20Helicopter%20.glb",
      "models/Ingenuity%20Mars%20Helicopter%20.glb"
    ],
    audioFiles: [
      "/app/static/audio/INGENVITY%20MARS.mp3",
      "/static/audio/INGENVITY%20MARS.mp3",
      "static/audio/INGENVITY%20MARS.mp3",
      "audio/INGENVITY%20MARS.mp3"
    ],
    color: "#00f0ff"
  }
};

/**
 * Fuzzy check if a given equipment ID or name is one of the 3 clickable equipments.
 */
function isEquipmentClickable(idOrName) {
  if (!idOrName) return false;
  const s = String(idOrName).toLowerCase().replace(/[^a-z0-9]/g, '');
  if (s.includes('opportunity') || s.includes('oppy') || s.includes('merb')) return true;
  if (s.includes('viking1') || s.includes('vikingone') || (s.includes('viking') && !s.includes('viking2') && !s.includes('vikingtwo'))) return true;
  if (s.includes('ingenuity') || s.includes('heli') || s.includes('marshelicopter')) return true;
  return false;
}

/**
 * Resolve which of the 3 equipments matches a given ID or name.
 */
function resolveEquipmentKey(idOrName) {
  if (!idOrName) return null;
  const s = String(idOrName).toLowerCase().replace(/[^a-z0-9]/g, '');
  if (s.includes('opportunity') || s.includes('oppy') || s.includes('merb')) return 'opportunity';
  if (s.includes('viking1') || s.includes('vikingone') || (s.includes('viking') && !s.includes('viking2') && !s.includes('vikingtwo'))) return 'viking-1';
  if (s.includes('ingenuity') || s.includes('heli') || s.includes('marshelicopter')) return 'ingenuity';
  return null;
}

/**
 * Moon Equipment Assets Configuration
 * Maps Apollo 11, Lunar Rover, and Surveyor 3 to their GLB 3D models and audio stories.
 */
const MOON_EQUIPMENT_ASSETS = {
  "apollo-11": {
    id: "apollo-11",
    name: "Apollo 11 'Eagle' LM",
    type: "Lander",
    aliasIds: ["apollo-11-lm", "apollo-11", "apollo11", "eagle", "apollo_11", "apollo11lm", "apollo"],
    modelFiles: [
      "/app/static/models/Apollo%2011.glb",
      "/app/static/models/apollo-11.glb",
      "/app/static/models/apollo11.glb",
      "/app/static/models/eagle.glb",
      "/app/static/models/lunar-module.glb",
      "/app/static/models/Viking%20Lander%20.glb",
      "/static/models/Apollo%2011.glb",
      "/static/models/apollo-11.glb",
      "static/models/apollo-11.glb"
    ],
    audioFiles: [
      "/app/static/audio/APOLLO%2011.mp3",
      "/app/static/audio/apollo-11.mp3",
      "/app/static/audio/apollo11.mp3",
      "/app/static/audio/eagle.mp3",
      "/app/static/audio/VIKING%20MARS.mp3",
      "/static/audio/apollo-11.mp3",
      "static/audio/apollo-11.mp3"
    ],
    color: "#fbbf24"
  },
  "apollo-15": {
    id: "apollo-15",
    name: "Apollo 15 & Lunar Rover",
    type: "Rover",
    aliasIds: ["apollo-15-lrv", "apollo-15", "apollo15", "lunar-rover", "lrv", "lunarrover", "rover1"],
    modelFiles: [
      "/app/static/models/Lunar%20Rover.glb",
      "/app/static/models/lunar-rover.glb",
      "/app/static/models/apollo-15.glb",
      "/app/static/models/apollo15.glb",
      "/app/static/models/Oppurtunity%20.glb",
      "/static/models/lunar-rover.glb",
      "static/models/lunar-rover.glb"
    ],
    audioFiles: [
      "/app/static/audio/LUNAR%20ROVER.mp3",
      "/app/static/audio/lunar-rover.mp3",
      "/app/static/audio/apollo-15.mp3",
      "/app/static/audio/SPIRIT%20AND%20OPPURTUNITY%20MARS.mp3",
      "/static/audio/lunar-rover.mp3",
      "static/audio/lunar-rover.mp3"
    ],
    color: "#00f0ff"
  },
  "surveyor-3": {
    id: "surveyor-3",
    name: "Surveyor 3 Lander",
    type: "Lander",
    aliasIds: ["surveyor-3-lander", "surveyor-3", "surveyor3", "surveyor", "surveyorlander"],
    modelFiles: [
      "/app/static/models/Surveyor%203.glb",
      "/app/static/models/surveyor-3.glb",
      "/app/static/models/surveyor3.glb",
      "/app/static/models/surveyor.glb",
      "/app/static/models/Viking%20Lander%20.glb",
      "/static/models/surveyor-3.glb",
      "static/models/surveyor-3.glb"
    ],
    audioFiles: [
      "/app/static/audio/SURVEYOR%203.mp3",
      "/app/static/audio/surveyor-3.mp3",
      "/app/static/audio/surveyor3.mp3",
      "/app/static/audio/surveyor.mp3",
      "/app/static/audio/VIKING%20MARS.mp3",
      "/static/audio/surveyor-3.mp3",
      "static/audio/surveyor-3.mp3"
    ],
    color: "#22c55e"
  }
};

/**
 * Fuzzy check if a given equipment ID or name is one of the clickable lunar equipments.
 */
function isMoonEquipmentClickable(idOrName) {
  if (!idOrName) return false;
  const s = String(idOrName).toLowerCase().replace(/[^a-z0-9]/g, '');
  if (s.includes('apollo11') || s.includes('eagle') || (s.includes('apollo') && !s.includes('apollo12') && !s.includes('apollo14') && !s.includes('apollo15') && !s.includes('apollo16') && !s.includes('apollo17'))) return true;
  if (s.includes('apollo15') || s.includes('lunarrover') || s.includes('lrv')) return true;
  if (s.includes('surveyor3') || s.includes('surveyor')) return true;
  return false;
}

/**
 * Resolve which of the lunar equipments matches a given ID or name.
 */
function resolveMoonEquipmentKey(idOrName) {
  if (!idOrName) return null;
  const s = String(idOrName).toLowerCase().replace(/[^a-z0-9]/g, '');
  if (s.includes('apollo11') || s.includes('eagle') || (s.includes('apollo') && !s.includes('apollo12') && !s.includes('apollo14') && !s.includes('apollo15') && !s.includes('apollo16') && !s.includes('apollo17'))) return 'apollo-11';
  if (s.includes('apollo15') || s.includes('lunarrover') || s.includes('lrv')) return 'apollo-15';
  if (s.includes('surveyor3') || s.includes('surveyor')) return 'surveyor-3';
  return null;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    MARS_EQUIPMENT_ASSETS,
    isEquipmentClickable,
    resolveEquipmentKey,
    MOON_EQUIPMENT_ASSETS,
    isMoonEquipmentClickable,
    resolveMoonEquipmentKey
  };
}
