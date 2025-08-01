// popup.js
document.addEventListener('DOMContentLoaded', function() {
  const statusDiv = document.getElementById('status');
  const outputDiv = document.getElementById('output');
  const testConnectionBtn = document.getElementById('testConnection');
  const openTabBtn = document.getElementById('openTab');
  
  // Check if background script is running
  function checkConnection() {
    chrome.runtime.sendMessage({action: 'ping'}, (response) => {
      if (chrome.runtime.lastError) {
        statusDiv.textContent = 'Extension Error';
        statusDiv.className = 'status disconnected';
        outputDiv.textContent = 'Error: ' + chrome.runtime.lastError.message;
      } else {
        statusDiv.textContent = 'Extension Running';
        statusDiv.className = 'status connected';
        outputDiv.textContent = 'Background script is active. Native messaging should be available.';
      }
    });
  }
  
  // Test connection button
  testConnectionBtn.addEventListener('click', function() {
    checkConnection();
  });
  
  // Test open tab button
  openTabBtn.addEventListener('click', function() {
    chrome.tabs.create({url: 'https://example.com'}, function(tab) {
      if (chrome.runtime.lastError) {
        outputDiv.textContent = 'Error creating tab: ' + chrome.runtime.lastError.message;
      } else {
        outputDiv.textContent = 'Successfully created tab: ' + tab.id;
      }
    });
  });
  
  // Initial connection check
  checkConnection();
});
