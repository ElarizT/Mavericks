export const extractFileName = (path?: string): string => {
  if (!path) return "";
  try {
    // First decode the URL-encoded string
    const decodedPath = decodeURIComponent(path);
    // Split by path separator and get the last part
    const parts = decodedPath.split(/[\/\\]/);
    return parts[parts.length - 1];
  } catch (error) {
    // If decoding fails, return the original string
    return path;
  }
};