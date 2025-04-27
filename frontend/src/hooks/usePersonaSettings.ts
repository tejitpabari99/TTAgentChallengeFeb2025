import { useState } from 'react';

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

export function usePersonaSettings() {
  const [personaSettings, setPersonaSettings] = useState<Record<string, PersonaSettings>>({});
  const [activePersonaIndex, setActivePersonaIndex] = useState<string | null>(null);

  const addPersona = () => {
    const newIndex = Object.keys(personaSettings).length.toString();
    setPersonaSettings(prev => ({
      ...prev,
      [newIndex]: {
        id: null,
        name: '',
        description: '',
        persona_prompt: '',
        persona_gpt_prompt: '',
        population_size: 5,
        agents: [],
        analysis: {
          analysis_prompt: '',
          analysis_gpt_prompt: '',
          extracted_result: {},
          combined_result: ''
        },
        qna: {
          qna_prompt: '',
          qna_gpt_prompt: '',
          extracted_result: {},
          combined_result: ''
        }
      }
    }));
  };

  const removePersona = (index: string) => {
    setPersonaSettings(prev => {
      const newSettings = { ...prev };
      delete newSettings[index];
      return newSettings;
    });
    if (activePersonaIndex === index) {
      setActivePersonaIndex(null);
    }
  };

  const updatePersona = (index: string, updates: Partial<PersonaSettings>) => {
    setPersonaSettings(prev => ({
      ...prev,
      [index]: {
        ...prev[index],
        ...updates
      }
    }));
  };

  const updatePersonaPrompts = (
    index: string,
    field: 'persona_prompt' | 'persona_gpt_prompt' | 'analysis_prompt' | 'analysis_gpt_prompt' | 'qna_prompt' | 'qna_gpt_prompt',
    value: string
  ) => {
    setPersonaSettings(prev => {
      const persona = prev[index];
      if (!persona) return prev;

      const newPersona = { ...persona };

      if (field === 'persona_prompt' || field === 'persona_gpt_prompt') {
        newPersona[field] = value;
      } else if (field.startsWith('analysis_')) {
        newPersona.analysis = {
          ...newPersona.analysis,
          [field]: value
        };
      } else if (field.startsWith('qna_')) {
        newPersona.qna = {
          ...newPersona.qna,
          [field]: value
        };
      }

      return {
        ...prev,
        [index]: newPersona
      };
    });
  };

  const openPersonaSettings = (index: string) => {
    setActivePersonaIndex(index);
  };

  const closePersonaSettings = () => {
    setActivePersonaIndex(null);
  };

  return {
    personaSettings,
    setPersonaSettings,
    activePersonaIndex,
    addPersona,
    removePersona,
    updatePersona,
    updatePersonaPrompts,
    openPersonaSettings,
    closePersonaSettings
  };
}
