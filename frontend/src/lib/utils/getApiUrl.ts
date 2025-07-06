/**
 * Centralized API URL construction utility
 * This ensures all API calls use the correct backend URL with /api prefix
 */

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || '';

/**
 * Constructs the full API URL for a given endpoint
 * @param endpoint - The API endpoint (should start with /)
 * @returns The complete API URL with /api prefix
 */
export function getApiUrl(endpoint: string): string {
  console.log('getApiUrl called with endpoint:', endpoint);
  console.log('API_URL from env:', API_URL);
  
  if (!API_URL) {
    console.warn('NEXT_PUBLIC_BACKEND_URL is not set');
    return `/api${endpoint}`;
  }
  
  // Ensure endpoint starts with /
  const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const finalUrl = `${API_URL}/api${normalizedEndpoint}`;
  
  console.log('Final API URL:', finalUrl);
  return finalUrl;
} 