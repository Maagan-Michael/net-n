import { FunctionComponent } from "react";
import clsx from "clsx";
import IconRoundBtn from "@components/inputs/iconRoundBtn";
import Customer from "@icons/customer.svg?react";
import House from "@icons/house.svg?react";
import Network from "@icons/network.svg?react";
import Computer from "@icons/computer.svg?react";
import { ConnectionsFilters as cf } from "@api/types";

interface IconFilterElemProps {
  sm?: boolean;
  onClick?: (e: React.MouseEvent<HTMLElement, MouseEvent>) => void;
  icon?: FunctionComponent<React.SVGAttributes<SVGElement>>;
  text?: string;
}

export const IconFilterElem = ({
  sm,
  icon: Icon,
  onClick,
  text,
}: IconFilterElemProps) => (
  <IconRoundBtn
    onClick={onClick}
    icon={Icon != null && <Icon className={clsx(sm ? "w-3 h-3" : "w-6 h-6")} />}
    className={sm ? "w-6 h-6 text-xs" : "w-10 h-10"}
    text={text}
  />
);

export const filtersMap: { [x: string]: IconFilterElemProps } = {
  [cf.customer]: { icon: Customer },
  [cf.address]: { icon: House },
  [cf.switch]: { icon: Network },
  [cf.up]: { icon: Computer },
  [cf.customerId]: { text: "ID" },
  [cf.enabled]: { text: "ON" },
};
