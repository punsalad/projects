// background.js
let nativePort = null;
let connecting = false;


// Connect to native messaging host
function connectToNativeHost() {
  if (nativePort || connecting) {
    console.log('Already connected (or connecting) — skipping');
    return;
  }
  connecting = true;

  try {
      nativePort = chrome.runtime.connectNative('com.chrome.api.bridge');
  } catch (e) {
      console.error('connectNative failed:', e);
      connecting = false;
      return;
  }
  
  nativePort.onMessage.addListener((message) => {
    handleNativeMessage(message);
  });
  
  nativePort.onDisconnect.addListener(() => {
    console.log('Native host disconnected:', chrome.runtime.lastError?.message);
    nativePort = null;
    connecting = false;
    // Use an alarm, not setTimeout — timers don't survive service worker teardown
    chrome.alarms.create('reconnect-native-host', { delayInMinutes: 0.1 });
  });
  
  connecting = false;
  console.log('Connected to native messaging host');
}

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'reconnect-native-host') {
      connectToNativeHost();
  }
});

// Handle messages from native host
async function handleNativeMessage(message) {
  try {
    const response = await executeCommand(message);
    if (nativePort) {
      nativePort.postMessage({
        id: message.id,
        success: true,
        result: response
      });
    }
  } catch (error) {
    console.error('Error executing command:', error);
    if (nativePort) {
      nativePort.postMessage({
        id: message.id,
        success: false,
        error: error.message
      });
    }
  }
}

// Execute Chrome API commands
async function executeCommand(message) {
  const { command, params } = message;
  
  switch (command) {
    case 'tabs.create':
      return await chrome.tabs.create(params);
    
    case 'tabs.query':
      return await chrome.tabs.query(params || {});
    
    case 'tabs.update':
      const { tabId, updateProperties } = params;
      return await chrome.tabs.update(tabId, updateProperties);
    
    case 'tabs.close':
      return await chrome.tabs.remove(params.tabId);
    
    case 'tabs.getCurrent':
      return await chrome.tabs.query({ active: true, currentWindow: true });
    
    case 'tabs.executeScript':
      const { tabId: scriptTabId, script } = params;
      return await chrome.scripting.executeScript({
        target: { tabId: scriptTabId },
        func: new Function(script)
      });
    
    case 'bookmarks.create':
      return await chrome.bookmarks.create(params);
    
    case 'bookmarks.get':
      return await chrome.bookmarks.get(params.id);
    
    case 'bookmarks.getTree':
      return await chrome.bookmarks.getTree();
    
    case 'bookmarks.search':
      return await chrome.bookmarks.search(params.query);
    
    case 'history.search':
      return await chrome.history.search(params);
    
    case 'history.deleteUrl':
      return await chrome.history.deleteUrl(params);
    
    case 'windows.create':
      return await chrome.windows.create(params);
    
    case 'windows.getAll':
      return await chrome.windows.getAll(params);
    
    case 'windows.getCurrent':
      return await chrome.windows.getCurrent();
    
    case 'storage.get':
      return await chrome.storage.local.get(params.keys);
    
    case 'storage.set':
      return await chrome.storage.local.set(params.items);
    
    case 'storage.remove':
      return await chrome.storage.local.remove(params.keys);
    
    default:
      throw new Error(`Unknown command: ${command}`);
  }
}

chrome.runtime.onStartup.addListener(() => {
  connectToNativeHost();
});

chrome.runtime.onInstalled.addListener(() => {
  connectToNativeHost();
});
connectToNativeHost();
