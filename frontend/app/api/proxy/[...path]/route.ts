import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  return proxyRequest(request, path, 'GET');
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  return proxyRequest(request, path, 'POST');
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  return proxyRequest(request, path, 'PUT');
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  return proxyRequest(request, path, 'DELETE');
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  return proxyRequest(request, path, 'PATCH');
}

async function proxyRequest(
  request: NextRequest,
  pathSegments: string[],
  method: string
) {
  try {
    const path = pathSegments.join('/');
    const backendUrl = `${BACKEND_URL}/${path}`;

    // Get request body for POST/PUT/PATCH
    let body: any = undefined;
    const headers: Record<string, string> = {};

    if (['POST', 'PUT', 'PATCH'].includes(method)) {
      const contentType = request.headers.get('content-type');

      // Handle multipart/form-data (file uploads) - forward as ArrayBuffer
      if (contentType?.includes('multipart/form-data')) {
        body = await request.arrayBuffer();
        // MUST forward content-type with boundary for multipart
        if (contentType) {
          headers['Content-Type'] = contentType;
        }
      } else {
        const text = await request.text();
        body = text || undefined;
        if (contentType) {
          headers['Content-Type'] = contentType;
        }
      }
    }

    // Forward other headers (excluding host and content-length)
    request.headers.forEach((value, key) => {
      const lowerKey = key.toLowerCase();
      if (lowerKey !== 'host' && lowerKey !== 'content-type' && lowerKey !== 'content-length') {
        headers[key] = value;
      }
    });

    console.log(`🔄 Proxying ${method} ${backendUrl}`);
    if (body) {
      console.log(`📦 Body type: ${body.constructor.name}, Content-Type: ${headers['Content-Type']}`);
    }

    // Make request to backend
    const response = await fetch(backendUrl, {
      method,
      headers,
      body,
      // @ts-ignore - duplex is needed for streaming
      duplex: 'half',
    });

    // Handle 204 No Content responses (like DELETE)
    if (response.status === 204) {
      return new NextResponse(null, {
        status: 204,
      });
    }

    // Check if response is binary (audio)
    const contentType = response.headers.get('content-type');
    if (contentType?.includes('audio/')) {
      const audioBuffer = await response.arrayBuffer();
      return new NextResponse(audioBuffer, {
        status: response.status,
        headers: {
          'Content-Type': contentType,
          'Content-Disposition': response.headers.get('content-disposition') || '',
        },
      });
    }

    // Get response body (JSON or text)
    const responseText = await response.text();
    let responseData;

    try {
      responseData = JSON.parse(responseText);
    } catch {
      responseData = responseText;
    }

    // Return response with same status code
    return NextResponse.json(responseData, {
      status: response.status,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error: any) {
    console.error('❌ Proxy error:', error.message);
    console.error('❌ Error details:', error);
    console.error('❌ Error stack:', error.stack);
    return NextResponse.json(
      { detail: `Backend service unavailable: ${error.message}` },
      { status: 503 }
    );
  }
}
