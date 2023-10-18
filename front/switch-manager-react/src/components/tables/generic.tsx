export interface TableHeaderCellProps {
    data: {
        id: string;
        title: string;
        separate?: boolean;
    }
}

export interface ColumnProps extends TableHeaderCellProps {
    render: (props: React.PropsWithChildren<TableHeaderCellProps>) => JSX.Element;
}

export interface DataProps<T> {
    data: T;
    render: ({ data }: { data: T }) => JSX.Element;
}

export interface TableProps<T> {
    columns: ColumnProps[];
    data: DataProps<T>[];
}

export const TableSeparator = () => (
    <div className="absolute min-h-[60%] w-[3px] rounded-full bg-neutral-100 block top-[20%] right-0"></div>
);

export const TableHeaderCell = ({  data: { title, separate = true }, children }: React.PropsWithChildren<TableHeaderCellProps>) => (
    <div
    key={title}
    className="relative h-full px-4 border-b-[3px] border-neutral-100"
        >
        {children ? children : <div className="font-light text-sm text-center">{title}</div>}
        {separate && <TableSeparator />}
    </div>
);

export function TableRow<T>({ data, children }: React.PropsWithChildren<{ data: T }>) {
    return (
        <div className="h-16 p-4 even:bg-neutral-100 rounded-md mt-1 grid grid-flow-col items-center">
            {/* {
                columns.map(
                    (column, index) => {
                        return (
                            <div key={column.title} className="px-4 text-sm text-center">
                                {row.data[column.title as keyof T] as string}
                            </div>
                        )
                    }
                )
            } */}
        </div>
    )
}

export default function Table<T extends { id: string }>({ columns, data }: TableProps<T>) {
    return (
        <div className="w-full">
            <section className="h-16 p-4 grid grid-flow-col">
            {
                columns.map((C, index) => <C.render key={C.data.id} data={C.data} />)
            }
            </section>
            <section>
            {
                data.map(
                    (R) => <R.render key={R.data.id} data={R.data} />
                )
            }
            </section>
        </div>
    )
}