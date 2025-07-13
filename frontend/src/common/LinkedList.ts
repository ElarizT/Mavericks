interface Node {
  id: string;
  name: string;
  color: string;
  nextId: string | null;
}

class LinkedList {
  private nodes: Map<string, Node>;
  private nextIds: Set<string>;
  private headNodes: Set<string> | null;
  private chains: Node[][] | null;

  constructor() {
    this.nodes = new Map<string, Node>();
    this.nextIds = new Set<string>();
    this.headNodes = null;
    this.chains = null;
  }

  private invalidateCache(): void {
    this.headNodes = null;
    this.chains = null;
  }

  hasNode(id: string): boolean {
    return this.nodes.has(id);
  }

  needsNextId(id: string): boolean {
    return this.nextIds.has(id);
  }

  addNode(node: Node): void {
    this.nodes.set(node.id, node);
    if (node.nextId) {
      this.nextIds.add(node.nextId);
    }
    this.invalidateCache();
  }

  getNodeById(id: string): Node | undefined {
    return this.nodes.get(id);
  }

  getNextNode(currentNode: Node): Node | undefined {
    if (!currentNode.nextId) {
      return undefined;
    }
    return this.nodes.get(currentNode.nextId);
  }

  // Validates if both the node's ID and nextId (if present) exist in the list
  validateNode(node: Node): boolean {
    // Check if the node's ID exists
    if (!this.hasNode(node.id)) {
      return false;
    }

    // If there's a nextId, check if it exists
    if (node.nextId !== null && !this.hasNode(node.nextId)) {
      return false;
    }

    return true;
  }

  private getHeadNodes(): Set<string> {
    if (this.headNodes === null) {
      this.headNodes = new Set<string>();
      const referencedIds = new Set<string>();
      
      // First pass: collect all referenced IDs
      for (const node of this.nodes.values()) {
        if (node.nextId) {
          referencedIds.add(node.nextId);
        }
      }
      
      // Second pass: find nodes not referenced by any nextId
      for (const node of this.nodes.values()) {
        if (!referencedIds.has(node.id)) {
          this.headNodes.add(node.id);
        }
      }
    }
    return this.headNodes;
  }

  getUnconnectedNodes(): Node[] {
    const headNodes = this.getHeadNodes();
    const result: Node[] = [];
    
    for (const id of headNodes) {
      const node = this.nodes.get(id);
      if (node) {
        result.push(node);
      }
    }
    
    return result;
  }

  removeUnconnectedNodes(): Node[] {
    const unconnectedNodes = this.getUnconnectedNodes();
    
    for (const node of unconnectedNodes) {
      this.nodes.delete(node.id);
      if (node.nextId) {
        this.nextIds.delete(node.nextId);
      }
    }
    
    this.invalidateCache();
    return unconnectedNodes;
  }

  splitIntoChains(): Node[][] {
    if (this.chains === null) {
      this.chains = [];
      const visited = new Set<string>();
      const headNodes = this.getHeadNodes();

      const buildChain = (startNode: Node): Node[] => {
        const chain: Node[] = [];
        let currentNode: Node | undefined = startNode;
        
        while (currentNode && !visited.has(currentNode.id)) {
          visited.add(currentNode.id);
          chain.push(currentNode);
          currentNode = currentNode.nextId ? this.nodes.get(currentNode.nextId) : undefined;
        }
        
        return chain;
      };

      for (const headId of headNodes) {
        const headNode = this.nodes.get(headId);
        if (headNode && !visited.has(headId)) {
          const chain = buildChain(headNode);
          if (chain.length > 0) {
            this.chains.push(chain);
          }
        }
      }
    }
    
    return this.chains;
  }

  getAllNodes(): Node[] {
    const chains = this.splitIntoChains();
    return chains.flat();
  }
}

export { LinkedList };
export type { Node };
 