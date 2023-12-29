const LoadingRow = () => (
  <div className="w-full h-20 lg:h-14 text-xs text-center grid grid-flow-col grid-cols-12 md:gap-x-4 lg:gap-x-8">
    <div className="h-full rounded-md bg-neutral-100 col-span-10"></div>
    <div className="h-full rounded-md bg-neutral-100 grow col-span-2"></div>
  </div>
);

export default LoadingRow;
