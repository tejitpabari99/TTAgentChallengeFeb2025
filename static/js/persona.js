// Initialize global personaSettings object
window.personaSettings = {};

// Initialize add persona button handler
function initAddPersonaHandler() {
    document.getElementById('addPersonaBtn')?.addEventListener('click', () => {
        const container = document.getElementById('personasContainer');
        const rowIndex = container.children.length;
        
        const personaRow = document.createElement('div');
        personaRow.className = 'persona-row';
        personaRow.dataset.index = rowIndex;
        personaRow.innerHTML = `
            <input type="text" name="personaName[${rowIndex}]" class="persona-input" placeholder="Persona name" required>
            <input type="text" name="personaDescription[${rowIndex}]" class="persona-input" placeholder="Persona description" required>
            <button type="button" class="persona-action-btn remove-persona-btn" title="Remove persona">
                <i class="fas fa-minus"></i>
            </button>
            <button type="button" class="persona-action-btn settings-persona-btn" title="Persona settings">
                <i class="fas fa-cog"></i>
            </button>
        `;
        
        // Add event listeners to the buttons
        const removeBtn = personaRow.querySelector('.remove-persona-btn');
        removeBtn.addEventListener('click', function() {
            personaRow.remove();
            // Remove persona settings when persona is deleted
            delete window.personaSettings[rowIndex];
        });
        
        const settingsBtn = personaRow.querySelector('.settings-persona-btn');
        settingsBtn.addEventListener('click', function() {
            const panel = document.getElementById('personaSettingsPanel');
            if (panel.classList.contains('open') && panel.dataset.personaIndex === rowIndex) {
                // If open for this persona, close it
                closePersonaSettings();
            } else {
                // Otherwise, open it for this persona
                openPersonaSettings(rowIndex);
            }
        });
        
        // Add input change listeners to reset results when inputs change
        const inputs = personaRow.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('change', resetResults);
        });
        
        container.appendChild(personaRow);
    });
}

// Settings panel functionality
function openPersonaSettings(personaIndex) {
    // Close any open settings panel first
    closePersonaSettings();
    
    // Get the persona data
    const personaRow = document.querySelector(`.persona-row[data-index="${personaIndex}"]`);
    if (!personaRow) return;
    
    const personaName = personaRow.querySelector('input[name^="personaName"]').value;
    const personaDesc = personaRow.querySelector('input[name^="personaDescription"]').value;
    
    // Update the panel title with the persona name
    const panelHeader = document.querySelector('.panel-header h3');
    if (panelHeader) {
        panelHeader.textContent = personaName ? `${personaName} Settings` : 'Persona Settings';
    }
    
    // Store the persona index in the panel
    const panel = document.getElementById('personaSettingsPanel');
    panel.dataset.personaIndex = personaIndex;
    
    // Open the panel
    panel.classList.add('open');
    
    // Initialize persona settings if not already set
    if (!window.personaSettings[personaIndex]) {
        window.personaSettings[personaIndex] = {
            id: null,
            name: personaName,
            description: personaDesc,
            persona_prompt: "",
            persona_gpt_prompt: "",
            population_size: 5,
            agents: [],
            analysis: {
                analysis_prompt: "",
                analysis_gpt_prompt: "",
                extracted_result: {},
                combined_result: ""
            },
            qna: {
                qna_prompt: "",
                qna_gpt_prompt: "",
                extracted_result: {},
                combined_result: ""
            }
        };
    }
    
    // Load settings from the stored data
    loadPersonaData(personaIndex);
}

// Initialize settings panel input change handlers
function initSettingsPanelInputHandlers() {
    document.querySelectorAll('#personaSettingsPanel input, #personaSettingsPanel textarea').forEach(input => {
        input.addEventListener('change', function() {
            const personaIndex = document.getElementById('personaSettingsPanel').dataset.personaIndex;
            if (!personaIndex) return;
            
            // Update the settings based on the input id
            switch (this.id) {
                case 'populationSize':
                    window.personaSettings[personaIndex].population_size = parseInt(this.value) || 5;
                    break;
                case 'personaPrompt':
                    window.personaSettings[personaIndex].persona_prompt = this.value;
                    break;
                case 'personaGptPrompt':
                    window.personaSettings[personaIndex].persona_gpt_prompt = this.value;
                    break;
                case 'analysisPrompt':
                    if (!window.personaSettings[personaIndex].analysis) window.personaSettings[personaIndex].analysis = {};
                    window.personaSettings[personaIndex].analysis.analysis_prompt = this.value;
                    break;
                case 'analysisGptPrompt':
                    if (!window.personaSettings[personaIndex].analysis) window.personaSettings[personaIndex].analysis = {};
                    window.personaSettings[personaIndex].analysis.analysis_gpt_prompt = this.value;
                    break;
                case 'qnaPrompt':
                    if (!window.personaSettings[personaIndex].qna) window.personaSettings[personaIndex].qna = {};
                    window.personaSettings[personaIndex].qna.qna_prompt = this.value;
                    break;
                case 'qnaGptPrompt':
                    if (!window.personaSettings[personaIndex].qna) window.personaSettings[personaIndex].qna = {};
                    window.personaSettings[personaIndex].qna.qna_gpt_prompt = this.value;
                    break;
            }
            
            // Reset results when settings change
            resetResults();
        });
    });
}

    // Load data for a persona
function loadPersonaData(personaIndex) {
    // Use stored settings if available
    if (window.personaSettings[personaIndex]) {
        const settings = window.personaSettings[personaIndex];
        
        // Populate the form fields with the data
        document.getElementById('populationSize').value = settings.population_size || 5;
        
        // Populate persona prompts
        document.getElementById('personaPrompt').value = settings.persona_prompt || '';
        document.getElementById('personaGptPrompt').value = settings.persona_gpt_prompt || '';
        
        // Populate analysis section
        if (settings.analysis) {
            document.getElementById('analysisPrompt').value = settings.analysis.analysis_prompt || '';
            document.getElementById('analysisGptPrompt').value = settings.analysis.analysis_gpt_prompt || '';
        }
        
        // Populate QNA section
        if (settings.qna) {
            document.getElementById('qnaPrompt').value = settings.qna.qna_prompt || '';
            document.getElementById('qnaGptPrompt').value = settings.qna.qna_gpt_prompt || '';
        }
        
        // Populate agents section
        const agentsContainer = document.getElementById('agentsContainer');
        agentsContainer.innerHTML = '';
        
        if (settings.agents && settings.agents.length > 0) {
            settings.agents.forEach((agent, index) => {
                const agentItem = document.createElement('div');
                agentItem.className = 'agent-item';
                agentItem.innerHTML = `
                    <div class="agent-header" data-index="${index}">
                        <i class="fas fa-plus expand-icon"></i>
                        <i class="fas fa-minus collapse-icon hidden"></i>
                        <span class="agent-name">${agent.agent_name || 'Agent ' + (index + 1)}</span>
                    </div>
                    <div class="agent-details hidden" data-index="${index}">
                        <div class="agent-detail-item">
                            <strong>Agent File:</strong> <span>${agent.agent_file || 'N/A'}</span>
                        </div>
                        <div class="agent-detail-item">
                            <strong>Agent Bio:</strong> <span>${agent.agent_description || 'N/A'}</span>
                        </div>
                    </div>
                `;
                
                // Add event listener to toggle agent details
                const header = agentItem.querySelector('.agent-header');
                header.addEventListener('click', function() {
                    const index = this.dataset.index;
                    const details = document.querySelector(`.agent-details[data-index="${index}"]`);
                    const expandIcon = this.querySelector('.expand-icon');
                    const collapseIcon = this.querySelector('.collapse-icon');
                    
                    if (details.classList.contains('hidden')) {
                        details.classList.remove('hidden');
                        expandIcon.classList.add('hidden');
                        collapseIcon.classList.remove('hidden');
                    } else {
                        details.classList.add('hidden');
                        expandIcon.classList.remove('hidden');
                        collapseIcon.classList.add('hidden');
                    }
                });
                
                agentsContainer.appendChild(agentItem);
            });
        } else {
            agentsContainer.innerHTML = '<div class="no-agents-msg">No agents available.</div>';
        }
    } else {
        // Use default placeholder data if no stored settings
        const placeholderData = {
            id: null,
            name: `Persona ${personaIndex + 1}`,
            description: 'Sample description',
            persona_prompt: 'Sample persona prompt',
            persona_gpt_prompt: '',
            population_size: 5,
            agents: [],
            analysis: {
                analysis_prompt: "Sample analysis prompt",
                analysis_gpt_prompt: "",
                extracted_result: {},
                combined_result: ""
            },
            qna: {
                qna_prompt: "Sample QNA prompt",
                qna_gpt_prompt: "",
                extracted_result: {},
                combined_result: ""
            }
        };
        
        // Store the placeholder data and populate UI
        window.personaSettings[personaIndex] = placeholderData;
        
        // Populate the form fields with the data
        document.getElementById('populationSize').value = placeholderData.population_size;
        
        // Populate persona prompts
        document.getElementById('personaPrompt').value = placeholderData.persona_prompt;
        document.getElementById('personaGptPrompt').value = placeholderData.persona_gpt_prompt;
        
        // Populate analysis section
        document.getElementById('analysisPrompt').value = placeholderData.analysis.analysis_prompt;
        document.getElementById('analysisGptPrompt').value = placeholderData.analysis.analysis_gpt_prompt;
        
        // Populate QNA section
        document.getElementById('qnaPrompt').value = placeholderData.qna.qna_prompt;
        document.getElementById('qnaGptPrompt').value = placeholderData.qna.qna_gpt_prompt;
        
        // Populate agents section
        const agentsContainer = document.getElementById('agentsContainer');
        agentsContainer.innerHTML = '';
        
        placeholderData.agents.forEach((agent, index) => {
            const agentItem = document.createElement('div');
            agentItem.className = 'agent-item';
            agentItem.innerHTML = `
                <div class="agent-header" data-index="${index}">
                    <i class="fas fa-plus expand-icon"></i>
                    <i class="fas fa-minus collapse-icon hidden"></i>
                    <span class="agent-name">${agent.agent_name}</span>
                </div>
                <div class="agent-details hidden" data-index="${index}">
                    <div class="agent-detail-item">
                        <strong>Agent File:</strong> <span>${agent.agent_file}</span>
                    </div>
                    <div class="agent-detail-item">
                        <strong>Agent Bio:</strong> <span>${agent.agent_description}</span>
                    </div>
                </div>
            `;
            
            // Add event listener to toggle agent details
            const header = agentItem.querySelector('.agent-header');
            header.addEventListener('click', function() {
                const index = this.dataset.index;
                const details = document.querySelector(`.agent-details[data-index="${index}"]`);
                const expandIcon = this.querySelector('.expand-icon');
                const collapseIcon = this.querySelector('.collapse-icon');
                
                if (details.classList.contains('hidden')) {
                    details.classList.remove('hidden');
                    expandIcon.classList.add('hidden');
                    collapseIcon.classList.remove('hidden');
                } else {
                    details.classList.add('hidden');
                    expandIcon.classList.remove('hidden');
                    collapseIcon.classList.add('hidden');
                }
            });
            
            agentsContainer.appendChild(agentItem);
        });
    }
}

// Export functions for use in other modules
window.openPersonaSettings = openPersonaSettings;
window.loadPersonaData = loadPersonaData;
window.initAddPersonaHandler = initAddPersonaHandler;
window.initSettingsPanelInputHandlers = initSettingsPanelInputHandlers;
