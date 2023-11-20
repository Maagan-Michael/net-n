import { useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import ConnectionForm from "./form";
import { useConnectionQuery } from "@api/queries/getConnection";

export default function Connection() {
  const { id } = useParams<{ id: string }>();
  if (!id) {
    // todo handle error route
    throw new Error("no id");
  }
  const { data, isLoading } = useConnectionQuery({ id });
  const navigate = useNavigate();
  const goBack = useCallback(
    () => navigate(`/${window.location.search}`),
    [navigate]
  );
  // todo handle error
  // todo create proper loader component
  return (
    <div className="fixed top-0 left-0 w-full h-full flex justify-center items-center z-20">
      {isLoading ? (
        <div>loading...</div>
      ) : (
        <ConnectionForm data={data} goBack={goBack} />
      )}
      <div
        className="absolute top-0 left-0 w-full h-full backdrop-blur-md flex justify-center items-center cursor-pointer hover:backdrop-blur-sm transition-all"
        onMouseDown={goBack}
      ></div>
    </div>
  );
}
