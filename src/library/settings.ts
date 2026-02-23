export const DEBUG = true;

export const DEVELOPMENT_ORIGIN = 'http://localhost:8000';

export const LIVE_ORIGIN = DEBUG ? DEVELOPMENT_ORIGIN : window.location.origin

export const API = new URL('/api/', DEVELOPMENT_ORIGIN).toString();

export const PRODUCTION_SERVER = new URL('/api/', window.location.origin);

export const BASE_URL = DEBUG ? API : PRODUCTION_SERVER;