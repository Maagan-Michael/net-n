import clsx from "clsx";

interface ColumnProps {
    title: string;
    render?: (value: any) => React.ReactNode;
    containerClass?: string;
    separatorClass?: string;
}

interface DataCol extends ColumnProps {
    property: string;
}

interface DataProps extends ColumnProps {
    _id: string;
}

interface TableProps {
    columns: ColumnProps[];
    //data: [DataProps[]];
}

export default function Table({ columns }: TableProps) {
    return (
        <table className="w-full table-fixed">
            <tr className="m-12 h-12 p-4">
                {
                    columns.map(
                        (column, index) => {
                            const render = column.render ? column.render(column) : column.title;
                            if (column.render) {
                            return column.render(column);
                        }
                        return (
                            <th
                            key={column.title}
                            className={clsx("relative h-full px-4 border-b-[3px] border-gray-200", column.containerClass)}
                                >
                                <div className="font-light text-sm">{render}</div>
                                <div className={
                                clsx(
                                        "absolute min-h-[60%] w-[3px] rounded-full bg-gray-200 block top-[20%] right-0",
                                        column.separatorClass
                                    )
                                }></div>
                            </th>
                        )
                    })
                }
            </tr>
        </table>
    )
}