"use client";

import { useRef } from "react";
import styles from "./ChangeBackgroundButton.module.css";
import { changeBgImage } from "@/actions/bgImageActions";

export default function ChangeBackgroundButton() {
  const fileInputRef = useRef(null);

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    try {
      await changeBgImage(formData);
      // Reload the page to see the new background
      window.location.reload();
    } catch (error) {
      console.error("Error changing background image:", error);
      alert("Failed to change background image. Please try again.");
    }
  };

  return (
    <div className={styles.container}>
      <button
        className={styles.changeBackgroundButton}
        onClick={handleButtonClick}
      >
        Change Background
      </button>
      <input
        type="file"
        ref={fileInputRef}
        className={styles.fileInput}
        accept="image/*"
        onChange={handleFileChange}
      />
    </div>
  );
}
