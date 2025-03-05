import { useState } from 'react';

interface PresentationInfo {
  title: string;
  description: string;
  intent: string;
}

interface PersonaSettings {
  id: string | null;
  name: string;
  description: string;
  persona_prompt: string;
  persona_gpt_prompt: string;
  population_size: number;
  agents: any[];
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
}

export function useFileHandler() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = async (
    e: React.ChangeEvent<HTMLInputElement>,
    setPresentationInfo: (info: PresentationInfo) => void,
    setPersonaSettings: (settings: Record<string, PersonaSettings>) => void
  ) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);

      if (file.name.toLowerCase().endsWith('.json')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          try {
            const jsonData = JSON.parse(e.target?.result as string);
            if (jsonData.ppt) {
              setPresentationInfo({
                title: jsonData.ppt.ppt_title || '',
                description: jsonData.ppt.ppt_description || '',
                intent: jsonData.ppt.ppt_intent || ''
              });
            }
            if (jsonData.personas && Array.isArray(jsonData.personas)) {
              const newPersonaSettings: Record<string, PersonaSettings> = {};
              jsonData.personas.forEach((persona: any, index: number) => {
                newPersonaSettings[index] = {
                  id: persona.id,
                  name: persona.name || '',
                  description: persona.description || '',
                  persona_prompt: persona.persona_prompt || '',
                  persona_gpt_prompt: persona.persona_gpt_prompt || '',
                  population_size: persona.population_size || 5,
                  agents: persona.agents || [],
                  analysis: persona.analysis || {
                    analysis_prompt: '',
                    analysis_gpt_prompt: '',
                    extracted_result: {},
                    combined_result: ''
                  },
                  qna: persona.qna || {
                    qna_prompt: '',
                    qna_gpt_prompt: '',
                    extracted_result: {},
                    combined_result: ''
                  }
                };
              });
              setPersonaSettings(newPersonaSettings);
            }
          } catch (error) {
            console.error('Error parsing JSON file:', error);
            alert('Error parsing JSON file. Please check the file format.');
          }
        };
        reader.readAsText(file);
      }
    }
  };

  return {
    selectedFile,
    handleFileChange
  };
}
