import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getProduct, generateImages, checkJobStatus } from '../services/api';
import { Download, Loader, CheckCircle, XCircle, ArrowLeft } from 'lucide-react';

const ProductDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [jobStatus, setJobStatus] = useState(null);

  useEffect(() => {
    loadProduct();
  }, [id]);

  useEffect(() => {
    let interval;
    if (jobStatus && jobStatus.status === 'processing') {
      interval = setInterval(() => {
        checkStatus(jobStatus.id);
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [jobStatus]);

  const loadProduct = async () => {
    try {
      const data = await getProduct(id);
      setProduct(data);
    } catch (error) {
      console.error('Error loading product:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateImages = async () => {
    setGenerating(true);
    try {
      const response = await generateImages(id);
      setJobStatus({
        id: response.job_id,
        status: 'processing'
      });
    } catch (error) {
      console.error('Error generating images:', error);
      setGenerating(false);
    }
  };

  const checkStatus = async (jobId) => {
    try {
      const status = await checkJobStatus(id, jobId);
      setJobStatus(status);
      
      if (status.status === 'completed' || status.status === 'failed') {
        setGenerating(false);
        loadProduct(); // Reload product to get new images
      }
    } catch (error) {
      console.error('Error checking job status:', error);
    }
  };

  const downloadImage = (url, filename) => {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const downloadAll = () => {
    product.images.forEach((image, index) => {
      if (image.kind !== 'original') {
        setTimeout(() => {
          downloadImage(image.url, `${product.sku}_${image.kind}.png`);
        }, index * 500);
      }
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Product not found</p>
      </div>
    );
  }

  const generatedImages = product.images.filter(img => img.kind !== 'original');
  const hasGeneratedImages = generatedImages.length > 0;

  return (
    <div className="px-4 sm:px-0">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate('/')}
          className="flex items-center text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="h-5 w-5 mr-1" />
          Back to Products
        </button>
        
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{product.name}</h1>
            <p className="mt-1 text-sm text-gray-500">SKU: {product.sku}</p>
            {product.description && (
              <p className="mt-2 text-gray-700">{product.description}</p>
            )}
          </div>
          
          <div className="flex space-x-3">
            {hasGeneratedImages && (
              <button
                onClick={downloadAll}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                <Download className="mr-2 h-4 w-4" />
                Download All
              </button>
            )}
            
            <button
              onClick={handleGenerateImages}
              disabled={generating}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {generating ? (
                <>
                  <Loader className="animate-spin mr-2 h-4 w-4" />
                  Generating...
                </>
              ) : (
                'Generate Images'
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Job Status */}
      {jobStatus && (
        <div className={`mb-6 p-4 rounded-lg ${
          jobStatus.status === 'completed' ? 'bg-green-50 border border-green-200' :
          jobStatus.status === 'failed' ? 'bg-red-50 border border-red-200' :
          'bg-blue-50 border border-blue-200'
        }`}>
          <div className="flex items-center">
            {jobStatus.status === 'completed' && <CheckCircle className="h-5 w-5 text-green-600 mr-2" />}
            {jobStatus.status === 'failed' && <XCircle className="h-5 w-5 text-red-600 mr-2" />}
            {jobStatus.status === 'processing' && <Loader className="animate-spin h-5 w-5 text-blue-600 mr-2" />}
            
            <div>
              <p className="font-medium">
                {jobStatus.status === 'completed' && 'Generation Complete!'}
                {jobStatus.status === 'failed' && 'Generation Failed'}
                {jobStatus.status === 'processing' && 'Generating Images...'}
              </p>
              {jobStatus.result && (
                <p className="text-sm mt-1">
                  Generated {jobStatus.result.generated_count} images
                </p>
              )}
              {jobStatus.error_message && (
                <p className="text-sm text-red-600 mt-1">{jobStatus.error_message}</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Images Grid */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Images</h2>
        
        {product.images.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            No images yet. Click "Generate Images" to create product variations.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {product.images.map((image) => (
              <div key={image.id} className="border rounded-lg overflow-hidden">
                <div className="aspect-square bg-gray-100 flex items-center justify-center p-4">
                  <img
                    src={image.url}
                    alt={`${product.name} - ${image.kind}`}
                    className="max-h-full max-w-full object-contain"
                  />
                </div>
                <div className="p-4 bg-white">
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="font-medium text-gray-900 capitalize">
                        {image.kind.replace('_', ' ')}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {new Date(image.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <button
                      onClick={() => downloadImage(image.url, `${product.sku}_${image.kind}.png`)}
                      className="p-2 text-gray-600 hover:text-blue-600 rounded-full hover:bg-gray-100"
                    >
                      <Download className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductDetailPage;