export default function TextButton({ label }: { label: string }) {
  return (
    <button className="bg-red-400 text-white px-4 py-2 rounded-md hover:shadow-md w-full font-light hover:bg-blue-300 transition-all">
      {label}
    </button>
  );
}
