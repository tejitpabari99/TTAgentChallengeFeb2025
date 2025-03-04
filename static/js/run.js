function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Initialize run button handler
function initRunButtonHandler() {
    document.getElementById('runButton')?.addEventListener('click', async () => {
        // Collect all data to send to the backend
        const pptName = document.getElementById('pptName').value;
        const pptFile = document.getElementById('pptFilePath').value;
        const pptTitle = document.getElementById('presentationTitle').value;
        const pptDescription = document.getElementById('presentationDescription').value;
        const pptIntent = document.getElementById('presentationIntent').value;
        
        // Collect persona data
        const personas = [];
        const personaRows = document.querySelectorAll('.persona-row');
        personaRows.forEach(row => {
            const rowIndex = row.dataset.index;
            const inputs = row.querySelectorAll('input');
            if (inputs[0].value.trim() && inputs[1].value.trim()) {
                
                personas.push({
                    id: null,
                    name: inputs[0].value.trim(),
                    description: inputs[1].value.trim(),
                    ...window.personaSettings[rowIndex]
                });
            }
        });
        
        // Show loading indicator
        const runButton = document.getElementById('runButton');
        const originalText = runButton.textContent;
        runButton.textContent = 'Processing...';
        runButton.disabled = true;

        console.log({
            ppt_name: pptName,
            ppt_file: pptFile,
            ppt_title: pptTitle,
            ppt_description: pptDescription,
            ppt_intent: pptIntent,
            personas: personas
        })
        
        try {
            // First, save the current state
            const saveResponse = await fetch('/update_presentation_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ppt_name: pptName,
                    ppt_file: pptFile,
                    ppt_title: pptTitle,
                    ppt_description: pptDescription,
                    ppt_intent: pptIntent,
                    personas: personas
                })
            });
            
            if (!saveResponse.ok) {
                throw new Error('Failed to save presentation information');
            }
            
            // Check if all personas have results before making API call
            const hasAllResults = personas.every(persona => 
                (persona.analysis?.extracted_result && Object.keys(persona.analysis.extracted_result).length > 0 && persona.analysis?.combined_result) &&
                (persona.qna?.extracted_result && Object.keys(persona.qna.extracted_result).length > 0 && persona.qna?.combined_result)
            );

            let result;
            if (hasAllResults) {
                // If all personas have results, use existing data
                result = {
                    ppt_name: pptName,
                    ppt_file: pptFile,
                    ppt_title: pptTitle,
                    ppt_description: pptDescription,
                    ppt_intent: pptIntent,
                    personas: personas
                };
                await sleep(5000);
            } else {
                // Otherwise, make API call
                const runResponse = await fetch('/run_analysis', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        ppt_name: pptName,
                        ppt_file: pptFile,
                        ppt_title: pptTitle,
                        ppt_description: pptDescription,
                        ppt_intent: pptIntent,
                        personas: personas
                    })
                });
                
                if (!runResponse.ok) {
                    throw new Error('Failed to run analysis');
                }
                
                result = await runResponse.json();
            }
            
            // Update the UI with the results
            updateResultsUI(result);
            
            // Show success message
            runButton.textContent = 'Completed!';
            runButton.style.backgroundColor = '#4CAF50'; // Success green
            
        } catch (error) {
            console.error('Error running analysis:', error);
            
            // Show error message
            runButton.textContent = 'Error!';
            runButton.style.backgroundColor = '#f44336'; // Error red
            
            setTimeout(() => {
                runButton.textContent = originalText;
                runButton.style.backgroundColor = ''; // Reset to default
                runButton.disabled = false;
            }, 3000);
            
            alert('Error running analysis. Please try again.');
        }
    });
}

// Function to update the UI with the analysis results
function updateResultsUI(results) {
    // Create or get the results container
    let resultsContainer = document.getElementById('resultsContainer');
    if (!resultsContainer) {
        resultsContainer = document.createElement('div');
        resultsContainer.id = 'resultsContainer';
        resultsContainer.className = 'results-container';
        document.querySelector('.container').appendChild(resultsContainer);
    } else {
        // Clear existing results
        resultsContainer.innerHTML = '';
    }
    
    // Create the results header
    const resultsHeader = document.createElement('h2');
    resultsHeader.textContent = 'Analysis Results';
    resultsContainer.appendChild(resultsHeader);
    
    // Process each persona's results
    if (results.personas && results.personas.length > 0) {
        results.personas.forEach(persona => {
            // Create persona section
            const personaSection = document.createElement('div');
            personaSection.className = 'persona-result-section';
            
            // Add persona header
            const personaHeader = document.createElement('h3');
            personaHeader.textContent = persona.name;
            personaSection.appendChild(personaHeader);
            
            // Add analysis results if available
            if (persona.analysis && persona.analysis.combined_result) {
                const analysisSection = document.createElement('div');
                analysisSection.className = 'analysis-section';
                
                const analysisHeader = document.createElement('h4');
                analysisHeader.textContent = 'Analysis';
                analysisSection.appendChild(analysisHeader);
                
                const analysisContent = document.createElement('div');
                analysisContent.className = 'analysis-content';
                
                // Try to parse the combined result as JSON
                try {
                    const analysisData = JSON.parse(persona.analysis.combined_result);
                    
                    // If it's an array, display each item
                    if (Array.isArray(analysisData)) {
                        analysisData.forEach(item => {
                            const itemElement = document.createElement('div');
                            itemElement.className = 'analysis-item';
                            
                            // Create content based on the item structure
                            if (typeof item === 'object') {
                                for (const [key, value] of Object.entries(item)) {
                                    const property = document.createElement('p');
                                    property.innerHTML = `<strong>${key}:</strong> ${value}`;
                                    itemElement.appendChild(property);
                                }
                            } else {
                                itemElement.textContent = item;
                            }
                            
                            analysisContent.appendChild(itemElement);
                        });
                    } else if (typeof analysisData === 'object') {
                        // If it's an object, display its properties
                        for (const [key, value] of Object.entries(analysisData)) {
                            const property = document.createElement('p');
                            property.innerHTML = `<strong>${key}:</strong> ${value}`;
                            analysisContent.appendChild(property);
                        }
                    } else {
                        // If it's a primitive value, display it directly
                        analysisContent.textContent = analysisData;
                    }
                } catch (e) {
                    // If parsing fails, try to convert markdown to HTML, fallback to simple newline replacement
                    try {
                        analysisContent.innerHTML = marked.parse(persona.analysis.combined_result);
                    } catch (markdownError) {
                        analysisContent.innerHTML = persona.analysis.combined_result.replace(/\n/g, '<br/>');
                    }
                }
                
                analysisSection.appendChild(analysisContent);
                personaSection.appendChild(analysisSection);
            }
            
            // Add QnA results if available
            if (persona.qna && persona.qna.combined_result) {
                const qnaSection = document.createElement('div');
                qnaSection.className = 'qna-section';
                
                const qnaHeader = document.createElement('h4');
                qnaHeader.textContent = 'Questions & Answers';
                qnaSection.appendChild(qnaHeader);
                
                const qnaContent = document.createElement('div');
                qnaContent.className = 'qna-content';
                
                // Try to parse the combined result as JSON
                try {
                    const qnaData = JSON.parse(persona.qna.combined_result);
                    
                    // If it's an array, display each item
                    if (Array.isArray(qnaData)) {
                        qnaData.forEach(item => {
                            const itemElement = document.createElement('div');
                            itemElement.className = 'qna-item';
                            
                            // Create content based on the item structure
                            if (typeof item === 'object') {
                                for (const [key, value] of Object.entries(item)) {
                                    const property = document.createElement('p');
                                    property.innerHTML = `<strong>${key}:</strong> ${value}`;
                                    itemElement.appendChild(property);
                                }
                            } else {
                                itemElement.textContent = item;
                            }
                            
                            qnaContent.appendChild(itemElement);
                        });
                    } else if (typeof qnaData === 'object') {
                        // If it's an object, display its properties
                        for (const [key, value] of Object.entries(qnaData)) {
                            const property = document.createElement('p');
                            property.innerHTML = `<strong>${key}:</strong> ${value}`;
                            qnaContent.appendChild(property);
                        }
                    } else {
                        // If it's a primitive value, display it directly
                        qnaContent.textContent = qnaData;
                    }
                } catch (e) {
                    // If parsing fails, try to convert markdown to HTML, fallback to simple newline replacement
                    try {
                        qnaContent.innerHTML = marked.parse(persona.qna.combined_result);
                    } catch (markdownError) {
                        qnaContent.innerHTML = persona.qna.combined_result.replace(/\n/g, '<br/>');
                    }
                }
                
                qnaSection.appendChild(qnaContent);
                personaSection.appendChild(qnaSection);
            }
            
            // Add the persona section to the results container
            resultsContainer.appendChild(personaSection);
        });
    } else {
        // No results available
        const noResults = document.createElement('p');
        noResults.textContent = 'No analysis results available.';
        resultsContainer.appendChild(noResults);
    }
    
    // Scroll to the results
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

// Export functions for use in other modules
window.initRunButtonHandler = initRunButtonHandler;
window.updateResultsUI = updateResultsUI;
