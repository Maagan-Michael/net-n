import { useTransition, animated } from "@react-spring/web";

export default function LoadingScreen() {
  const [transitions, api] = useTransition(true, () => ({
    from: { transform: "scale(1.0)" },
    enter: { transform: "scale(1.0)", delay: 1000 },
    leave: { transform: "scale(0.0)", delay: 5000 },
    config: {
      duration: 5000,
    },
  }));
  return transitions((style) => (
    <animated.div
      className="fixed top-0 left-0 w-screen h-screen flex items-center justify-center"
      style={style}
    >
      <span className="font-thin text-xl md:text-3xl animate-pulse">
        SwitchManager
      </span>
    </animated.div>
  ));
}
