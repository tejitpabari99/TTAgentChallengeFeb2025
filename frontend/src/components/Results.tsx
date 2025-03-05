'use client';

import { marked } from 'marked';
import { useState } from 'react';
import styles from './Results.module.css';

interface ResultsProps {
  results: {
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
  };
}

interface CollapsibleProps {
  title: string;
  defaultCollapsed?: boolean;
  children: React.ReactNode;
}

function Collapsible({ title, defaultCollapsed = true, children }: CollapsibleProps) {
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed);

  return (
    <div className={styles.collapsible}>
      <button
        className={`${styles.collapsibleHeader} ${isCollapsed ? styles.collapsed : ''}`}
        onClick={() => setIsCollapsed(!isCollapsed)}
      >
        <span className={styles.collapsibleTitle}>{title}</span>
        <span className={styles.collapsibleIcon}>{isCollapsed ? '+' : '-'}</span>
      </button>
      {!isCollapsed && (
        <div className={styles.collapsibleContent}>
          {children}
        </div>
      )}
    </div>
  );
}

export function Results({ results }: ResultsProps) {
  const renderContent = (content: string) => {
    try {
      // Try to parse as markdown first
      return <div dangerouslySetInnerHTML={{ __html: marked.parse(content) }} />;
    } catch (markdownError) {
      // If markdown parsing fails, treat as plain text with line breaks
      return <p dangerouslySetInnerHTML={{ __html: content.replace(/\n/g, '<br/>') }} />;
    }
  };

  return (
    <div className={styles.resultsContainer}>
      <h2>Analysis Results</h2>
      <div className={styles.personaList}>
          {results.personas.map((persona, index) => (
            <Collapsible key={`results-${index}`} title={`${persona.name} Results`} defaultCollapsed={false}>
              <div className={styles.personaResultSection}>
                {persona.analysis && persona.analysis.combined_result && (
                  <div className={styles.analysisSection}>
                    <Collapsible title="Analysis" defaultCollapsed={true}>
                      <div className={styles.analysisContent}>
                        {renderContent(persona.analysis.combined_result)}
                      </div>
                    </Collapsible>
                  </div>
                )}

                {persona.qna && persona.qna.combined_result && (
                  <div className={styles.qnaSection}>
                    <Collapsible title="Questions & Answers" defaultCollapsed={true}>
                      <div className={styles.qnaContent}>
                        {renderContent(persona.qna.combined_result)}
                      </div>
                    </Collapsible>
                  </div>
                )}
              </div>
            </Collapsible>
          ))}
        </div>
    </div>
  );
}
