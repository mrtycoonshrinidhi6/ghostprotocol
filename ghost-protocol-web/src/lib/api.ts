import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Types
export interface SystemStatus {
    status: string;
    active_agents: number;
    timestamp: string;
}

// API Methods
export async function getSystemStatus(): Promise<SystemStatus> {
    const { data } = await api.get<SystemStatus>('/system_status');
    return data;
}

export async function runDeathDetection(userId: string): Promise<DeathDetectionResponse> {
    const { data } = await api.post<DeathDetectionResponse>('/detect_death', { user_id: userId });
    return data;
}

export async function scanAssets(userId: string, sessionId: string): Promise<AssetScanResponse> {
    const { data } = await api.post<AssetScanResponse>('/scan_assets', { user_id: userId, session_id: sessionId });
    return data;
}

export async function getAssets(userId: string): Promise<AssetScanResponse> {
    // Assuming GET endpoint exists or reusing scan for now
    const { data } = await api.get<AssetScanResponse>(`/assets?user_id=${userId}`);
    return data;
}

export async function deployContract(userId: string, sessionId: string): Promise<ContractResponse> {
    const { data } = await api.post<ContractResponse>('/execute_will', { user_id: userId, session_id: sessionId });
    return data;
}

export async function getContractStatus(sessionId: string): Promise<ContractResponse> {
    const { data } = await api.get<ContractResponse>(`/session/${sessionId}`); // Using session status as proxy
    return data;
}

export async function sendMemorialMessage(userId: string, sessionId: string, message: string): Promise<ChatResponse> {
    const { data } = await api.post<ChatResponse>('/memorial_chat', {
        user_id: userId,
        session_id: sessionId,
        recipient: "memorial_twin",
        message
    });
    return data;
}
