import { useCallback, useEffect, useRef } from "react";
export default function useTimeout() {
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | undefined>(
    undefined
  );
  useEffect(() => {
    return () => {
      if (timeoutRef.current != null) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);
  return useCallback((cb: () => void, delay: number) => {
    const timeout = timeoutRef.current;
    if (timeout != null) {
      clearTimeout(timeout);
    }
    timeoutRef.current = setTimeout(cb, delay);
  }, []);
}
