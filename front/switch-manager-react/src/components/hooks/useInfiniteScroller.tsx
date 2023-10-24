import { useCallback, useRef, useState, useEffect } from "react";

export default function useInfiniteScroller(callback?: () => void) {
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
            rootMargin: "0px",
            threshold: 0.1,
          }
        );
        observer.current.observe(el);
        console.log(observer.current);
      }
    },
    [callback]
  );
  useEffect(() => {
    //cleanup observer here
  }, []);
  return onReady;
}
