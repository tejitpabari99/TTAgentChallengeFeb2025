'use client';

import { useEffect } from 'react';
import styles from './PersonaSettings.module.css';

interface PersonaSettingsProps {
  isOpen: boolean;
  personaIndex: string | null;
  personaSettings: any;
  onClose: () => void;
  onUpdatePrompts: (
    index: string,
    field: 'persona_prompt' | 'persona_gpt_prompt' | 'analysis_prompt' | 'analysis_gpt_prompt' | 'qna_prompt' | 'qna_gpt_prompt',
    value: string
  ) => void;
}

export function PersonaSettings({
  isOpen,
  personaIndex,
  personaSettings,
  onClose,
  onUpdatePrompts
}: PersonaSettingsProps) {
  const persona = personaIndex !== null ? personaSettings[personaIndex] : null;

  if (!isOpen || !persona) return null;

  return (
    <div className={`${styles.personaSettingsPanel} ${isOpen ? styles.open : ''}`}>
      <div className={styles.panelHeader}>
        <h3>{persona.name || 'Persona'} Settings</h3>
        <button 
          type="button" 
          className={styles.closePanelBtn}
          onClick={onClose}
        >
          <i className="fas fa-times"></i>
        </button>
      </div>

      <div className={styles.panelContent}>
        <div className={styles.settingsSection}>
          <h3>General Settings</h3>
          <div className={styles.formGroup}>
            <label htmlFor="populationSize">Population Size</label>
            <input
              type="number"
              id="populationSize"
              name="populationSize"
              value={persona.population_size}
              min="1"
              onChange={(e) => personaIndex && onUpdatePrompts(personaIndex, 'persona_prompt', e.target.value)}
              className={styles.input}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="personaGptPrompt">Persona GPT Prompt</label>
            <textarea
              id="personaGptPrompt"
              name="personaGptPrompt"
              value={persona.persona_gpt_prompt}
              onChange={(e) => personaIndex && onUpdatePrompts(personaIndex, 'persona_gpt_prompt', e.target.value)}
              className={`${styles.textarea} ${styles.fixedHeightPrompt}`}
              rows={10}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="personaPrompt">Persona Prompt</label>
            <textarea
              id="personaPrompt"
              name="personaPrompt"
              value={persona.persona_prompt}
              onChange={(e) => personaIndex && onUpdatePrompts(personaIndex, 'persona_prompt', e.target.value)}
              className={`${styles.textarea} ${styles.fixedHeightPrompt}`}
              rows={10}
            />
          </div>
        </div>

        <div className={styles.settingsSection}>
          <h3>Agents</h3>
          <div className={styles.agentsContainer}>
            {persona.agents.length > 0 ? (
              persona.agents.map((agent: any, index: number) => (
                <div key={index} className={styles.agentItem}>
                  <div className={styles.agentHeader}>
                    <i className="fas fa-plus expand-icon"></i>
                    <i className="fas fa-minus collapse-icon hidden"></i>
                    <span className={styles.agentName}>{agent.agent_name || `Agent ${index + 1}`}</span>
                  </div>
                  <div className={`${styles.agentDetails} ${styles.hidden}`}>
                    <div className={styles.agentDetailItem}>
                      <strong>Agent File:</strong> <span>{agent.agent_file || 'N/A'}</span>
                    </div>
                    <div className={styles.agentDetailItem}>
                      <strong>Agent Bio:</strong> <span>{agent.agent_description || 'N/A'}</span>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className={styles.noAgentsMsg}>No agents available.</div>
            )}
          </div>
        </div>

        <div className={styles.settingsSection}>
          <h3>Analysis Settings</h3>
          <div className={styles.formGroup}>
            <label htmlFor="analysisGptPrompt">Analysis GPT Prompt</label>
            <textarea
              id="analysisGptPrompt"
              name="analysisGptPrompt"
              value={persona.analysis.analysis_gpt_prompt}
              onChange={(e) => personaIndex && onUpdatePrompts(personaIndex, 'analysis_gpt_prompt', e.target.value)}
              className={`${styles.textarea} ${styles.fixedHeightPrompt}`}
              rows={10}
            />
          </div>
          <div className={styles.formGroup}>
            <label htmlFor="analysisPrompt">Analysis Prompt</label>
            <textarea
              id="analysisPrompt"
              name="analysisPrompt"
              value={persona.analysis.analysis_prompt}
              onChange={(e) => personaIndex && onUpdatePrompts(personaIndex, 'analysis_prompt', e.target.value)}
              className={`${styles.textarea} ${styles.fixedHeightPrompt}`}
              rows={10}
            />
          </div>
        </div>

        <div className={styles.settingsSection}>
          <h3>QNA Settings</h3>
          <div className={styles.formGroup}>
            <label htmlFor="qnaGptPrompt">QNA GPT Prompt</label>
            <textarea
              id="qnaGptPrompt"
              name="qnaGptPrompt"
              value={persona.qna.qna_gpt_prompt}
              onChange={(e) => personaIndex && onUpdatePrompts(personaIndex, 'qna_gpt_prompt', e.target.value)}
              className={`${styles.textarea} ${styles.fixedHeightPrompt}`}
              rows={10}
            />
          </div>
          <div className={styles.formGroup}>
            <label htmlFor="qnaPrompt">QNA Prompt</label>
            <textarea
              id="qnaPrompt"
              name="qnaPrompt"
              value={persona.qna.qna_prompt}
              onChange={(e) => personaIndex && onUpdatePrompts(personaIndex, 'qna_prompt', e.target.value)}
              className={`${styles.textarea} ${styles.fixedHeightPrompt}`}
              rows={10}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
