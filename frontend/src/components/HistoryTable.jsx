import React from "react";

export default function HistoryTable({ history, onDetails }) {
  return (
    <table className="w-full border mt-3 bg-white">
      <thead>
        <tr>
          <th className="border px-2">ID</th>
          <th className="border px-2">URL</th>
          <th className="border px-2">Title</th>
          <th className="border px-2">Date Generated</th>
          <th className="border px-2"></th>
        </tr>
      </thead>
      <tbody>
        {history.map(row => (
          <tr key={row.id}>
            <td className="border px-2">{row.id}</td>
            <td className="border px-2 truncate max-w-xs" title={row.url}>{row.url}</td>
            <td className="border px-2">{row.title}</td>
            <td className="border px-2">{new Date(row.date_generated).toLocaleString()}</td>
            <td className="border px-2">
              <button onClick={() => onDetails(row.id)} className="text-blue-500 underline">Details</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
