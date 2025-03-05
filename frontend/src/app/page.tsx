'use client';

import { useState } from 'react';
import styles from './page.module.css';
import { useFileHandler } from '@/hooks/useFileHandler';
import { usePersonaSettings } from '@/hooks/usePersonaSettings';
import { PersonaSettings as PersonaSettingsComponent } from '@/components/PersonaSettings';
import { Results } from '@/components/Results';

interface AnalysisResults {
  ppt: {
    ppt_id: string | null;
    ppt_name: string;
    ppt_file: string;
    ppt_title: string;
    ppt_description: string;
    ppt_intent: string;
    ppt_content: Record<string, any>;
  };
  personas: Array<{
    id: string | null;
    name: string;
    description: string;
    persona_prompt: string;
    persona_gpt_prompt: string;
    population_size: number;
    agents: Array<{
      agent_id: string;
      agent_name: string;
      agent_description: string;
      agent_file: string;
    }>;
    analysis: {
      analysis_prompt: string;
      analysis_gpt_prompt: string;
      extracted_result: Record<string, any>;
      combined_result: string;
    };
    qna: {
      qna_prompt: string;
      qna_gpt_prompt: string;
      extracted_result: Record<string, any>;
      combined_result: string;
    };
  }>;
}

export default function Home() {
  const [results, setResults] = useState<AnalysisResults | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [presentationInfo, setPresentationInfo] = useState({
    title: '',
    description: '',
    intent: ''
  });

  const { selectedFile, handleFileChange } = useFileHandler();
  const {
    personaSettings,
    setPersonaSettings,
    activePersonaIndex,
    addPersona,
    removePersona,
    updatePersona,
    updatePersonaPrompts,
    openPersonaSettings,
    closePersonaSettings
  } = usePersonaSettings();

  const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

  const handleRunAnalysis = async () => {
    if (!selectedFile) {
      alert('Please select a file first');
      return;
    }

    // Close the settings panel before running analysis
    closePersonaSettings();
    setIsAnalyzing(true);

    try {
      // Check if all personas have results before making API call
      const hasAllResults = Object.values(personaSettings).every(persona =>
        (persona.analysis?.extracted_result && Object.keys(persona.analysis.extracted_result).length > 0 && persona.analysis?.combined_result) &&
        (persona.qna?.extracted_result && Object.keys(persona.qna.extracted_result).length > 0 && persona.qna?.combined_result)
      );

      let result: any;
      if (hasAllResults) {
        // If all personas have results, use existing data
        result = {
          ppt: {
            ppt_id: null,
            ppt_name: selectedFile.name,
            ppt_file: selectedFile.name,
            ppt_title: presentationInfo.title,
            ppt_description: presentationInfo.description,
            ppt_intent: presentationInfo.intent,
            ppt_content: {} // This would be populated from the file content
          },
          personas: Object.values(personaSettings)
        };
        await sleep(5000); // Wait for 5 seconds to simulate processing
      } else {
        // Otherwise, make API call
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('ppt_title', presentationInfo.title);
        formData.append('ppt_description', presentationInfo.description);
        formData.append('ppt_intent', presentationInfo.intent);
        formData.append('personas', JSON.stringify(Object.values(personaSettings)));

        const response = await fetch('/api/run_analysis', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          throw new Error('Failed to run analysis');
        }

        result = await response.json();
      }

      setResults(result);
    } catch (error) {
      console.error('Error running analysis:', error);
      alert('Error running analysis. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <main className={styles.main}>
      <main className={styles.innerMain}>
      <h1 style={{ textAlign: "center" }}>PowerPoint Content Extractor</h1>

      <div className={styles.instructions}>
        <div className={styles.instructionsHeader}>
          <h3>Instructions</h3>
          <button
            className={styles.collapseButton}
            onClick={() => {
              const content = document.querySelector(`.${styles.instructionsContent}`);
              if (content) {
                content.classList.toggle(styles.collapsed);
              }
            }}
          >
            <i className="fas fa-chevron-up"></i>
          </button>
        </div>
        <div className={styles.instructionsContent}>
          <ul>
            <li>Select either
              <ul>
                <li>A PowerPoint file (.pptx) to extract content</li>
                <li>A JSON config file (.json) to load existing configuration</li>
              </ul>
            </li>
            <li>Click "Upload" to process the file</li>
            <li>For PowerPoint files, the tool will extract text and notes</li>
            <li>For JSON files, the tool will populate all form fields with the saved configuration</li>
            <li>Maximum file size: 16MB</li>
          </ul>
        </div>
      </div>

      <div className={styles.card}>
        <h2>Upload File</h2>
        <form onSubmit={(e) => e.preventDefault()}>
          <div
            className={styles.uploadArea}
            onClick={() => document.getElementById('fileInput')?.click()}
          >
            <label className={styles.uploadLabel}>
              Click or drag file here to upload
            </label>
            <input
              id="fileInput"
              type="file"
              accept=".pptx,.json"
              onChange={(e) => handleFileChange(e, setPresentationInfo, setPersonaSettings)}
              className={styles.fileInput}
            />
            {selectedFile && (
              <div className={styles.selectedFile}>
                Selected file: {selectedFile.name}
              </div>
            )}
          </div>
        </form>
      </div>

      <div className={styles.card}>
        <h2>Presentation Information</h2>
        <div className={styles.formGroup}>
          <label htmlFor="presentationTitle">Title</label>
          <input
            type="text"
            id="presentationTitle"
            value={presentationInfo.title}
            onChange={(e) => setPresentationInfo(prev => ({ ...prev, title: e.target.value }))}
            className={styles.input}
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="presentationDescription">Presentation Description</label>
          <textarea
            id="presentationDescription"
            value={presentationInfo.description}
            onChange={(e) => setPresentationInfo(prev => ({ ...prev, description: e.target.value }))}
            className={styles.textarea}
            rows={3}
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="presentationIntent">Intent</label>
          <textarea
            id="presentationIntent"
            value={presentationInfo.intent}
            onChange={(e) => setPresentationInfo(prev => ({ ...prev, intent: e.target.value }))}
            className={styles.textarea}
            rows={2}
          />
        </div>
      </div>

      <div className={styles.card}>
        <h2>Personas</h2>
        <div className={styles.personasHeader}>
          <h3>Add Persona</h3>
          <button onClick={addPersona} className={styles.addPersonaBtn}>
            <i className="fas fa-plus"></i>
          </button>
        </div>

        <div className={styles.personasContainer}>
          {Object.entries(personaSettings).map(([index, persona]) => (
            <div key={index} className={styles.personaRow}>
              <input
                type="text"
                placeholder="Persona name"
                value={persona.name}
                onChange={(e) => updatePersona(index, { name: e.target.value, description: persona.description })}
                className={styles.input}
              />
              <input
                type="text"
                placeholder="Persona description"
                value={persona.description}
                onChange={(e) => updatePersona(index, { name: persona.name, description: e.target.value })}
                className={styles.input}
              />
              <button
                onClick={() => removePersona(index)}
                className={styles.removePersonaBtn}
              >
                <i className="fas fa-minus"></i>
              </button>
              <button
                onClick={() => openPersonaSettings(index)}
                className={styles.settingsPersonaBtn}
              >
                <i className="fas fa-cog"></i>
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className={styles.buttonContainer}>
        <button
          onClick={handleRunAnalysis}
          className={styles.runButton}
          disabled={isAnalyzing}
        >
          {isAnalyzing ? 'Analyzing...' : 'Run Analysis'}
        </button>
      </div>

      <PersonaSettingsComponent
        isOpen={activePersonaIndex !== null}
        personaIndex={activePersonaIndex}
        personaSettings={personaSettings}
        onClose={closePersonaSettings}
        onUpdatePrompts={updatePersonaPrompts}
      />
    </main>
    {results && <Results results={results} />}
    </main>
  );
}
