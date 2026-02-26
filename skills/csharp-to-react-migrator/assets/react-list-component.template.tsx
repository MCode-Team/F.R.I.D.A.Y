import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link, useSearchParams } from 'react-router-dom'
import { entityService } from '@/services/entityService'
import type { Entity } from '@/types/entity'

/**
 * Entity List Page
 * 
 * Features:
 * - Paginated list
 * - Search functionality
 * - Delete with confirmation
 * - Loading states
 * - Error handling
 */

export function EntityList() {
  const [searchParams, setSearchParams] = useSearchParams()
  const searchTerm = searchParams.get('search') || ''
  const page = parseInt(searchParams.get('page') || '1', 10)
  const [localSearch, setLocalSearch] = useState(searchTerm)
  const queryClient = useQueryClient()

  // Fetch entities
  const { data, isLoading, error } = useQuery({
    queryKey: ['entities', { searchTerm, page }],
    queryFn: () => entityService.getAll({ searchTerm, page, limit: 10 })
  })

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: entityService.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['entities'] })
    }
  })

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setSearchParams({ search: localSearch, page: '1' })
  }

  const handlePageChange = (newPage: number) => {
    setSearchParams({ 
      search: searchTerm, 
      page: newPage.toString() 
    })
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      try {
        await deleteMutation.mutateAsync(id)
      } catch (error) {
        alert('Failed to delete item')
      }
    }
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          Error loading data. Please try again.
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Entities</h1>
        <Link
          to="/entities/create"
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
        >
          Create New
        </Link>
      </div>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={localSearch}
            onChange={(e) => setLocalSearch(e.target.value)}
            placeholder="Search entities..."
            className="flex-1 px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded"
          >
            Search
          </button>
        </div>
      </form>

      {/* Data Table */}
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <table className="min-w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Description
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data?.data.map((entity: Entity) => (
              <tr key={entity.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">
                    {entity.name}
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="text-sm text-gray-500">
                    {entity.description || '-'}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(entity.createdAt).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <Link
                    to={`/entities/${entity.id}`}
                    className="text-blue-600 hover:text-blue-900"
                  >
                    View
                  </Link>
                  <Link
                    to={`/entities/${entity.id}/edit`}
                    className="text-yellow-600 hover:text-yellow-900"
                  >
                    Edit
                  </Link>
                  <button
                    onClick={() => handleDelete(entity.id)}
                    className="text-red-600 hover:text-red-900"
                    disabled={deleteMutation.isPending}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Empty State */}
        {data?.data.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">No entities found.</p>
            <Link
              to="/entities/create"
              className="text-blue-600 hover:text-blue-900 mt-2 inline-block"
            >
              Create your first entity
            </Link>
          </div>
        )}
      </div>

      {/* Pagination */}
      {data && data.pagination.totalPages > 1 && (
        <div className="mt-6 flex justify-center">
          <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
            {/* Previous Button */}
            <button
              onClick={() => handlePageChange(page - 1)}
              disabled={page === 1}
              className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>

            {/* Page Numbers */}
            {Array.from({ length: data.pagination.totalPages }, (_, i) => i + 1)
              .filter(pageNum => {
                // Show first page, last page, and pages around current page
                return pageNum === 1 || 
                       pageNum === data.pagination.totalPages ||
                       Math.abs(pageNum - page) <= 2
              })
              .map((pageNum, index, array) => (
                <span key={pageNum}>
                  {/* Show ellipsis if there's a gap */}
                  {index > 0 && array[index - 1] !== pageNum - 1 && (
                    <span className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                      ...
                    </span>
                  )}
                  <button
                    onClick={() => handlePageChange(pageNum)}
                    className={`relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
                      pageNum === page
                        ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                        : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                    }`}
                  >
                    {pageNum}
                  </button>
                </span>
              ))}

            {/* Next Button */}
            <button
              onClick={() => handlePageChange(page + 1)}
              disabled={page === data.pagination.totalPages}
              className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </nav>
        </div>
      )}
    </div>
  )
}

/**
 * Usage:
 * 
 * 1. Add route to router:
 *    { path: '/entities', element: <EntityList /> }
 * 
 * 2. Create service file:
 *    src/services/entityService.ts
 * 
 * 3. Create type file:
 *    src/types/entity.ts
 * 
 * 4. Customize:
 *    - Replace 'Entity' with your actual entity name
 *    - Update table columns as needed
 *    - Add filters if necessary
 *    - Adjust pagination size
 */
