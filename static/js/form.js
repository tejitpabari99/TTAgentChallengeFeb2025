// Initialize file input handlers
function initFileInputHandlers() {
    document.getElementById('pptFile')?.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            const file = this.files[0];
            const fileName = file.name;
            const filePath = this.value;

            // Update hidden fields
            document.getElementById('pptName').value = fileName;
            document.getElementById('pptFilePath').value = fileName;

            // If it's a JSON file, parse and populate form
            if (fileName.toLowerCase().endsWith('.json')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    try {
                        const jsonData = JSON.parse(e.target.result);
                        populateFormFromJson(jsonData);
                    } catch (error) {
                        console.error('Error parsing JSON file:', error);
                        alert('Error parsing JSON file. Please check the file format.');
                    }
                };
                reader.readAsText(file);
            }
        }
    });
}

// Function to populate form fields from JSON data
function populateFormFromJson(data) {
    // Populate presentation info
    if (data.ppt) {
        document.getElementById('presentationTitle').value = data.ppt.ppt_title || '';
        document.getElementById('presentationDescription').value = data.ppt.ppt_description || '';
        document.getElementById('presentationIntent').value = data.ppt.ppt_intent || '';
    }

    // Clear existing personas
    const personasContainer = document.getElementById('personasContainer');
    personasContainer.innerHTML = '';

    // Add personas from JSON
    if (data.personas && Array.isArray(data.personas)) {
        // Initialize global personaSettings if not exists
        if (typeof window.personaSettings === 'undefined') {
            window.personaSettings = {};
        }

        data.personas.forEach((persona, index) => {
            // Create persona row
            const addPersonaBtn = document.getElementById('addPersonaBtn');
            addPersonaBtn.click(); // This creates a new persona row

            // Get the newly created row
            const personaRow = personasContainer.lastElementChild;
            const inputs = personaRow.querySelectorAll('input');
            
            // Set name and description
            inputs[0].value = persona.name || '';
            inputs[1].value = persona.description || '';

            // Store persona data
            window.personaSettings[index] = {
                id: persona.id,
                name: persona.name,
                description: persona.description,
                persona_prompt: persona.persona_prompt || '',
                persona_gpt_prompt: persona.persona_gpt_prompt || '',
                population_size: persona.population_size || 5,
                agents: persona.agents || [],
                analysis: persona.analysis || {
                    analysis_prompt: '',
                    analysis_gpt_prompt: '',
                    extracted_result: { },
                    combined_result: ''
                },
                qna: persona.qna || {
                    qna_prompt: '',
                    qna_gpt_prompt: '',
                    extracted_result: { },
                    combined_result: ''
                }
            };
        });
    }
    console.log(window.personaSettings);
}

// Export functions for use in other modules
window.initFileInputHandlers = initFileInputHandlers;
window.populateFormFromJson = populateFormFromJson;
