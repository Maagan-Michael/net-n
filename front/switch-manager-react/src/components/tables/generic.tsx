export interface TableProps<T extends { id: string }> {
  data: T[];
  renderRow: ({ data }: React.PropsWithChildren<{ data: T }>) => JSX.Element;
  renderHeader: JSX.Element;
  onReady?: (el: HTMLDivElement | null) => void;
}

export const TableSeparator = () => (
  <div className="separator absolute min-h-[60%] w-[2px] rounded-full bg-neutral-100 block top-[20%] right-0"></div>
);

export function Table({
  data,
  renderHeader,
  renderRow: Row,
  onReady,
}: TableProps<any>) {
  return (
    <div className="w-full">
      <section className="flex flex-col gap-y-1 md:gap-y-1 lg:gap-y-4">
        {renderHeader}
        {data.map((d, idx) => {
          if (idx === data.length - 1) {
            return (
              <div key={d.id} ref={(el) => onReady && onReady(el)}>
                <Row data={d} />
              </div>
            );
          }
          return <Row key={d.id} data={d} />;
        })}
      </section>
    </div>
  );
}
