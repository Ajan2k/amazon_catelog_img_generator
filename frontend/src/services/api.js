import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/products';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Add request interceptor to ensure headers are always set
api.interceptors.request.use(
  (config) => {
    // Only set JSON content type if it's NOT a file upload
    if (!config.headers['Content-Type'] && !(config.data instanceof FormData)) {
      config.headers['Content-Type'] = 'application/json';
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Products
export const createProduct = async (formData) => {
  // Let Axios and the browser handle the Content-Type automatically
  const response = await api.post('/products/', formData);
  return response.data;
};

export const getProducts = async () => {
  const response = await api.get('/products/');
  return response.data;
};

export const getProduct = async (id) => {
  const response = await api.get(`/products/${id}/`);
  return response.data;
};

// Generate Images - FIXED VERSION
export const generateImages = async (productId, templateIds = []) => {
  const response = await api.post(
    `/products/${productId}/generate_images/`,
    JSON.stringify({ template_ids: templateIds }),
    {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    }
  );
  return response.data;
};

export const checkJobStatus = async (productId, jobId) => {
  const response = await api.get(`/products/${productId}/job_status/`, {
    params: { job_id: jobId },
  });
  return response.data;
};

// Templates
export const getTemplates = async (kind = null) => {
  const url = kind ? `/templates/by_kind/?kind=${kind}` : '/templates/';
  const response = await api.get(url);
  return response.data;
};

// Logos
export const getLogos = async () => {
  const response = await api.get('/logos/');
  return response.data;
};

export const getDefaultLogo = async () => {
  const response = await api.get('/logos/default/');
  return response.data;
};

export const uploadLogo = async (formData) => {
  const response = await api.post('/logos/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export default api;