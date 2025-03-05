import { NextRequest, NextResponse } from 'next/server';
import { writeFile } from 'fs/promises';
import path from 'path';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;
    const pptTitle = formData.get('ppt_title');
    const pptDescription = formData.get('ppt_description');
    const pptIntent = formData.get('ppt_intent');
    const personas = JSON.parse(formData.get('personas') as string);

    if (!file) {
      return NextResponse.json(
        { error: 'No file uploaded' },
        { status: 400 }
      );
    }

    // Convert file to buffer
    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    // Save file to temporary location
    const tempDir = path.join(process.cwd(), 'temp');
    const filePath = path.join(tempDir, file.name);
    await writeFile(filePath, buffer);

    // TODO: Add your PowerPoint analysis logic here
    // For now, return mock response
    const mockResponse = {
      ppt_name: file.name,
      ppt_file: filePath,
      ppt_title: pptTitle,
      ppt_description: pptDescription,
      ppt_intent: pptIntent,
      personas: personas.map((persona: any) => ({
        ...persona,
        analysis: {
          ...persona.analysis,
          extracted_result: {
            key_points: ['Mock point 1', 'Mock point 2'],
            sentiment: 'positive'
          },
          combined_result: 'Mock analysis result'
        },
        qna: {
          ...persona.qna,
          extracted_result: {
            questions: ['Mock Q1', 'Mock Q2'],
            answers: ['Mock A1', 'Mock A2']
          },
          combined_result: 'Mock QnA result'
        }
      }))
    };

    return NextResponse.json(mockResponse);
  } catch (error) {
    console.error('Error processing request:', error);
    return NextResponse.json(
      { error: 'Error processing request' },
      { status: 500 }
    );
  }
}
