// Elysia.js Route Template
// Copy this template when creating new routes

import { Elysia, t } from 'elysia'
import { prisma } from '../db'
import { isAuthenticated } from '../middleware/auth'

export const entityRoutes = new Elysia({ prefix: '/api/entities' })
  .use(isAuthenticated)
  
  // GET /api/entities - List all entities
  .get('/', async ({ query }) => {
    const { page = 1, limit = 10, searchTerm } = query
    const skip = (page - 1) * limit

    const where = searchTerm
      ? {
          OR: [
            { name: { contains: searchTerm } },
            { description: { contains: searchTerm } }
          ]
        }
      : {}

    const [entities, total] = await Promise.all([
      prisma.entity.findMany({
        where,
        orderBy: { createdAt: 'desc' },
        skip,
        take: limit
      }),
      prisma.entity.count({ where })
    ])

    return {
      data: entities,
      pagination: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit)
      }
    }
  }, {
    query: t.Object({
      searchTerm: t.Optional(t.String()),
      page: t.Optional(t.Number({ minimum: 1 })),
      limit: t.Optional(t.Number({ minimum: 1, maximum: 100 }))
    }),
    response: t.Object({
      data: t.Array(t.Object({
        id: t.Number(),
        name: t.String(),
        description: t.Nullable(t.String()),
        createdAt: t.Date(),
        updatedAt: t.Nullable(t.Date())
      })),
      pagination: t.Object({
        page: t.Number(),
        limit: t.Number(),
        total: t.Number(),
        totalPages: t.Number()
      })
    }),
    detail: {
      summary: 'List all entities',
      tags: ['Entities']
    }
  })

  // GET /api/entities/:id - Get entity by ID
  .get('/:id', async ({ params, set }) => {
    const entity = await prisma.entity.findUnique({
      where: { id: params.id }
    })

    if (!entity) {
      set.status = 404
      throw new Error('Entity not found')
    }

    return entity
  }, {
    params: t.Object({
      id: t.Number()
    }),
    response: t.Object({
      id: t.Number(),
      name: t.String(),
      description: t.Nullable(t.String()),
      createdAt: t.Date(),
      updatedAt: t.Nullable(t.Date())
    }),
    detail: {
      summary: 'Get entity by ID',
      tags: ['Entities']
    }
  })

  // POST /api/entities - Create new entity
  .post('/', async ({ body, set }) => {
    // Check if entity already exists
    const existing = await prisma.entity.findFirst({
      where: { name: body.name }
    })

    if (existing) {
      set.status = 400
      throw new Error('Entity with this name already exists')
    }

    const entity = await prisma.entity.create({
      data: body
    })

    set.status = 201
    return entity
  }, {
    body: t.Object({
      name: t.String({ minLength: 1, maxLength: 100 }),
      description: t.Optional(t.String({ maxLength: 500 }))
    }),
    response: t.Object({
      id: t.Number(),
      name: t.String(),
      description: t.Nullable(t.String()),
      createdAt: t.Date()
    }),
    detail: {
      summary: 'Create new entity',
      tags: ['Entities']
    }
  })

  // PUT /api/entities/:id - Update entity
  .put('/:id', async ({ params, body, set }) => {
    const existing = await prisma.entity.findUnique({
      where: { id: params.id }
    })

    if (!existing) {
      set.status = 404
      throw new Error('Entity not found')
    }

    // Check if new name conflicts with other entities
    if (body.name) {
      const conflict = await prisma.entity.findFirst({
        where: {
          AND: [
            { id: { not: params.id } },
            { name: body.name }
          ]
        }
      })

      if (conflict) {
        set.status = 400
        throw new Error('Entity with this name already exists')
      }
    }

    const entity = await prisma.entity.update({
      where: { id: params.id },
      data: body
    })

    return entity
  }, {
    params: t.Object({
      id: t.Number()
    }),
    body: t.Object({
      name: t.Optional(t.String({ minLength: 1, maxLength: 100 })),
      description: t.Optional(t.String({ maxLength: 500 }))
    }),
    response: t.Object({
      id: t.Number(),
      name: t.String(),
      description: t.Nullable(t.String()),
      createdAt: t.Date(),
      updatedAt: t.Nullable(t.Date())
    }),
    detail: {
      summary: 'Update entity',
      tags: ['Entities']
    }
  })

  // DELETE /api/entities/:id - Delete entity
  .delete('/:id', async ({ params, set }) => {
    const existing = await prisma.entity.findUnique({
      where: { id: params.id }
    })

    if (!existing) {
      set.status = 404
      throw new Error('Entity not found')
    }

    await prisma.entity.delete({
      where: { id: params.id }
    })

    set.status = 204
    return { message: 'Entity deleted successfully' }
  }, {
    params: t.Object({
      id: t.Number()
    }),
    response: t.Object({
      message: t.String()
    }),
    detail: {
      summary: 'Delete entity',
      tags: ['Entities']
    }
  })

// Register routes in main app:
// import { entityRoutes } from './routes/entities'
// app.use(entityRoutes)
