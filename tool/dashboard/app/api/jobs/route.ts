import { NextResponse } from 'next/server';
import { getAllJobs } from '@/lib/getJobs';

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const jobs = getAllJobs();
    return NextResponse.json({ jobs });
  } catch (error: any) {
    console.error('API Error:', error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
