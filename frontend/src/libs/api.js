import { ApiClient } from "./apiClient";

const HTTPS = process.env.HTTPS == "true";
const API_URL = HTTPS
  ? process.env.API_BASE_HTTPS_URL
  : process.env.API_BASE_URL;
const apiClient = new ApiClient(API_URL);

// API functions
export const getTasks = async (queryParams = {}) => {
  const params = new URLSearchParams(queryParams);
  return apiClient.get(`/todos/?${params.toString()}`);
};

export const getTask = async (id) => {
  return apiClient.get(`/todos/${id}/`);
};

export const createTask = async (data) => {
  return apiClient.post(`/todos/`, data);
};

export const updateTask = async (id, data) => {
  return apiClient.patch(`/todos/${id}/`, data);
};

export const deleteTask = async (id) => {
  return apiClient.delete(`/todos/${id}/`);
};

export const completeTask = async (id, data) => {
  return apiClient.post(`/todos/${id}/complete/`, data);
};

export const incompleteTask = async (id, data) => {
  return apiClient.post(`/todos/${id}/incomplete/`, data);
};

export const getBgImage = async () => {
  return apiClient.get(`/bgimages/1/`);
};

export const changeBgImage = async (data) => {
  return apiClient.patch(`/bgimages/1/`, data, true);
};
