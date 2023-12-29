import { useCallback, useRef, useEffect } from "react";

export default function useInfiniteScroller(
  callback?: () => void,
  { rootMargin, threshold }: IntersectionObserverInit = {}
) {
  const ref = useRef<HTMLDivElement>(null);
  const observer = useRef<IntersectionObserver | null>(null);
  const onReady = useCallback(
    (el: HTMLDivElement | null) => {
      if (el) {
        //@ts-ignore
        ref.current = el;
        if (observer.current) {
          observer.current.disconnect();
        }
        observer.current = new IntersectionObserver(
          (entries, observer) => {
            entries.forEach((entry) => {
              if (entry.isIntersecting) {
                if (entry.target === ref.current) {
                  callback && callback();
                }
              }
            });
          },
          {
            root: null,
            rootMargin,
            threshold,
          }
        );
        observer.current.observe(el);
      }
    },
    [callback, rootMargin, threshold]
  );
  useEffect(() => {
    return () => {
      if (observer.current) {
        observer.current.disconnect();
      }
    };
  }, []);
  return onReady;
}
