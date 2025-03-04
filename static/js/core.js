// Global variables to store persona settings
let personaSettings = {};

// Initialize event listeners when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // File selection event
    initFileSelectionHandlers();
    
    // Expandable content handlers
    initExpandableContentHandlers();
    
    // Add persona button handler
    initAddPersonaHandler();
    
    // Close settings panel button handler
    initCloseSettingsPanelHandler();
    
    // File input styling and functionality
    initFileInputHandlers();
    
    // Settings panel input change handlers
    initSettingsPanelInputHandlers();
    
    // Run button handler
    initRunButtonHandler();
    
    // Initialize settings button toggle
    initSettingsButtonToggle();
});

// Initialize file selection handlers
function initFileSelectionHandlers() {
    document.getElementById('pptFile')?.addEventListener('change', function(e) {
        if (this.files && this.files.length > 0) {
            const fileName = this.files[0].name;
            const filePath = this.value; // This will be a fake path for security reasons
            
            // Update the file name and path fields if they exist
            const nameField = document.getElementById('pptName');
            const pathField = document.getElementById('pptFilePath');
            
            if (nameField) nameField.value = fileName;
            if (pathField) pathField.value = filePath;
        }
    });
}

// Initialize expandable content handlers
function initExpandableContentHandlers() {
    document.querySelectorAll('.expandable-label').forEach(label => {
        label.addEventListener('click', function() {
            const expandIcon = this.querySelector('.expand-icon');
            const collapseIcon = this.querySelector('.collapse-icon');
            const content = this.closest('.form-group').querySelector('.expandable-content');
            
            if (content.classList.contains('hidden')) {
                content.classList.remove('hidden');
                expandIcon.classList.add('hidden');
                collapseIcon.classList.remove('hidden');
            } else {
                content.classList.add('hidden');
                expandIcon.classList.remove('hidden');
                collapseIcon.classList.add('hidden');
            }
        });
    });
}

// Initialize close settings panel handler
function initCloseSettingsPanelHandler() {
    document.querySelector('.close-panel-btn')?.addEventListener('click', closePersonaSettings);
}

// Initialize settings button toggle functionality
function initSettingsButtonToggle() {
    document.querySelectorAll('.settings-persona-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const personaRow = this.closest('.persona-row');
            const rowIndex = personaRow.dataset.index;
            
            // Check if settings panel is already open for this persona
            const panel = document.getElementById('personaSettingsPanel');
            if (panel.classList.contains('open') && panel.dataset.personaIndex === rowIndex) {
                // If open for this persona, close it
                closePersonaSettings();
            } else {
                // Otherwise, open it for this persona
                openPersonaSettings(rowIndex);
            }
        });
    });
}

// Reset results when inputs change
function resetResults() {
    // Reset agent_response, extracted_result, and combined_result for all personas
    for (const personaIndex in personaSettings) {
        if (personaSettings[personaIndex].analysis) {
            personaSettings[personaIndex].analysis.agent_responses = {};
            personaSettings[personaIndex].analysis.extracted_result = {};
            personaSettings[personaIndex].analysis.combined_result = "";
        }
        
        if (personaSettings[personaIndex].qna) {
            personaSettings[personaIndex].qna.agent_responses = {};
            personaSettings[personaIndex].qna.extracted_result = {};
            personaSettings[personaIndex].qna.combined_result = "";
        }
    }
}

// Close persona settings panel
function closePersonaSettings() {
    const panel = document.getElementById('personaSettingsPanel');
    panel.classList.remove('open');
    delete panel.dataset.personaIndex;
}

// Export functions and variables for use in other modules
window.personaSettings = personaSettings;
window.resetResults = resetResults;
window.closePersonaSettings = closePersonaSettings;
window.initSettingsButtonToggle = initSettingsButtonToggle;
