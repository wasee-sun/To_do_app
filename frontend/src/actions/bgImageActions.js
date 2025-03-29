"use server";

import {
  getBgImage as getBgImageApi,
  changeBgImage as changeBgImageApi,
} from "@/libs/api";

export async function getBgImage() {
  try {
    return await getBgImageApi();
  } catch (error) {
    console.error("Error in getBgImage action:", error);
    throw new Error("Failed to get background image");
  }
}

export async function changeBgImage(formData) {
  try {
    return await changeBgImageApi(formData);
  } catch (error) {
    console.error("Error in changeBgImage action:", error);
    throw new Error("Failed to change background image");
  }
}
