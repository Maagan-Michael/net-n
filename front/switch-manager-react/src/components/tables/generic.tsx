export interface TableProps<T extends { id: string }> {
  data: T[];
  renderRow: ({ data }: React.PropsWithChildren<{ data: T }>) => JSX.Element;
  renderHeader: JSX.Element;
}

export const TableSeparator = () => (
  <div className="absolute min-h-[60%] w-[2px] rounded-full bg-neutral-100 block top-[20%] right-0"></div>
);

export function Table<T extends { id: string }>({
  data,
  renderHeader,
  renderRow: Row,
}: TableProps<T>) {
  return (
    <div className="w-full">
      <section className="flex flex-col gap-y-8 pt-4">
        {renderHeader}
        {data.map((d) => (
          <Row key={d.id} data={d} />
        ))}
      </section>
    </div>
  );
}
