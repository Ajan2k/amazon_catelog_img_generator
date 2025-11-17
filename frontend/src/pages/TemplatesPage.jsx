import React, { useState, useEffect } from 'react';
import { getTemplates } from '../services/api';
import { Layout, CheckCircle, XCircle } from 'lucide-react';

const TemplatesPage = () => {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const data = await getTemplates();
      setTemplates(data);
    } catch (error) {
      console.error('Error loading templates:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="px-4 sm:px-0">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Templates</h1>
        <p className="mt-2 text-sm text-gray-700">
          Available templates for generating product images
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {templates.map((template) => (
          <div key={template.id} className="bg-white shadow rounded-lg overflow-hidden">
            {template.background_url && (
              <div className="h-48 bg-gray-100">
                <img
                  src={template.background_url}
                  alt={template.name}
                  className="w-full h-full object-cover"
                />
              </div>
            )}
            
            <div className="p-5">
              <div className="flex items-start justify-between">
                <div className="flex items-center">
                  <Layout className="h-5 w-5 text-gray-400 mr-2" />
                  <h3 className="text-lg font-medium text-gray-900">
                    {template.name}
                  </h3>
                </div>
                {template.is_active ? (
                  <CheckCircle className="h-5 w-5 text-green-500" />
                ) : (
                  <XCircle className="h-5 w-5 text-gray-400" />
                )}
              </div>
              
              {template.description && (
                <p className="mt-2 text-sm text-gray-600">
                  {template.description}
                </p>
              )}
              
              <div className="mt-3">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 capitalize">
                  {template.kind}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {templates.length === 0 && (
        <div className="text-center py-12">
          <Layout className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No templates</h3>
          <p className="mt-1 text-sm text-gray-500">
            No templates are currently available.
          </p>
        </div>
      )}
    </div>
  );
};

export default TemplatesPage;