'use client';

import { marked } from 'marked';
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
      name: string;
      analysis: {
        extracted_result: Record<string, any>;
        combined_result: string;
      };
      qna: {
        extracted_result: Record<string, any>;
        combined_result: string;
      };
    }>;
  };
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
      <div className={styles.presentationInfo}>
        <h3>Presentation Information</h3>
        <p><strong>Title:</strong> {results.ppt.ppt_title}</p>
        <p><strong>Description:</strong> {results.ppt.ppt_description}</p>
        <p><strong>Intent:</strong> {results.ppt.ppt_intent}</p>
      </div>
      {results.personas.map((persona, index) => (
        <div key={index} className={styles.personaResultSection}>
          <h3>{persona.name}</h3>

          {persona.analysis && persona.analysis.combined_result && (
            <div className={styles.analysisSection}>
              <h4>Analysis</h4>
              <div className={styles.analysisContent}>
                {renderContent(persona.analysis.combined_result)}
              </div>
            </div>
          )}

          {persona.qna && persona.qna.combined_result && (
            <div className={styles.qnaSection}>
              <h4>Questions & Answers</h4>
              <div className={styles.qnaContent}>
                {renderContent(persona.qna.combined_result)}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
