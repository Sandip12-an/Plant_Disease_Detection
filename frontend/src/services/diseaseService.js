import { request } from './api';

export const diseaseService = {
  // Model inference on leaf photo
  async predict(file) {
    const formData = new FormData();
    formData.append('file', file);
    return request('/predict', {
      method: 'POST',
      body: formData,
    });
  },

  // Scan History
  async getHistory(limit = 20, offset = 0) {
    return request(`/history?limit=${limit}&offset=${offset}`);
  },

  async getHistoryDetail(id) {
    return request(`/history/${id}`);
  },

  async deleteHistory(id) {
    return request(`/history/${id}`, {
      method: 'DELETE',
    });
  },

  // Crop & Disease Encyclopedia
  async getCrops() {
    return request('/diseases/crops');
  },

  async getDiseases(params = {}) {
    const query = new URLSearchParams();
    if (params.crop) query.append('crop', params.crop);
    if (params.search) query.append('search', params.search);
    if (params.limit) query.append('limit', params.limit);
    if (params.offset) query.append('offset', params.offset);

    return request(`/diseases?${query.toString()}`);
  },

  async getDiseaseDetail(diseaseId) {
    return request(`/diseases/${encodeURIComponent(diseaseId)}`);
  },

  // Health probe
  async checkHealth() {
    return request('/health');
  },
};
