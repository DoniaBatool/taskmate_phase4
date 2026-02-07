import { NextResponse } from 'next/server'

/**
 * Health check endpoint for container orchestration.
 * Returns a simple healthy status for liveness probes.
 */
export async function GET() {
  return NextResponse.json({ status: 'healthy' })
}
