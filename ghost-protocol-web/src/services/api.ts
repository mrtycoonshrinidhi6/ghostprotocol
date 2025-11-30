import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface SystemStatus {
    status: string;
    active_agents: number;
    uptime: string;
    assets_secured: number;
    version: string;
}

export const fetchSystemStatus = async (): Promise<SystemStatus> => {
    try {
        const response = await api.get<SystemStatus>('/system_status');
        return response.data;
    } catch (error) {
        console.error('Failed to fetch system status:', error);
        // Return fallback data if API fails (to prevent UI crash during dev)
        return {
            status: 'Offline',
            active_agents: 0,
            uptime: '0%',
            assets_secured: 0,
            version: 'Unknown',
        };
    }
};
